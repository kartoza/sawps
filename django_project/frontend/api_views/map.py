"""API Views related to map."""
from typing import Tuple, List
import requests
from django.db import connection
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from frontend.models.context_layer import ContextLayer
from frontend.serializers.context_layer import ContextLayerSerializer
from frontend.utils.map import get_map_template_style
from frontend.models import (
    Erf,
    Holding,
    FarmPortion,
    ParentFarm
)
from frontend.serializers.parcel import (
    ErfParcelSerializer,
    HoldingParcelSerializer,
    FarmPortionParcelSerializer,
    ParentFarmParcelSerializer
)

User = get_user_model()


class ContextLayerList(APIView):
    """Fetch context layers."""
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        """Retrieve all context layers."""
        layers = ContextLayer.objects.all().order_by('id')
        return Response(
            status=200,
            data=ContextLayerSerializer(layers, many=True).data
        )


class MapStyles(APIView):
    """Fetch map styles."""
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        """Retrieve map styles."""
        theme = self.request.GET.get('theme', 'light')
        styles = get_map_template_style(
            self.request,
            0 if theme == 'light' else 1
        )
        return Response(
            status=200,
            data=styles,
            content_type="application/json"
        )


class PropertiesLayerMVTTiles(APIView):
    """Dynamic Vector Tile for properties layer."""
    permission_classes = [IsAuthenticated]

    def generate_tile(self, sql, query_values):
        rows = []
        tile = []
        with connection.cursor() as cursor:
            raw_sql = (
                'SELECT ST_AsMVT(tile.*, \'properties\', '
                '4096, \'geom\', \'id\') '
                'FROM ('
                f'{sql}'
                ') AS tile '
            )
            cursor.execute(raw_sql, query_values)
            rows = cursor.fetchall()
            for row in rows:
                tile.append(bytes(row[0]))
        return tile

    def generate_query_for_map(
            self,
            user: User,
            z: int,
            x: int,
            y: int,) -> Tuple[str, List[str]]:
        sql = (
            'SELECT p.id, p.name, '
            'ST_AsMVTGeom('
            '  ST_Transform(p.geometry, 3857), '
            '  TileBBox(%s, %s, %s, 3857)) as geom '
            'from property p '
            'where p.geometry && TileBBox(%s, %s, %s, 4326) '
        )
        query_values = [
            z, x, y,
            z, x, y,
        ]
        if not user.is_superuser:
            sql = (
                sql +
                'AND (p.created_by_id=%s OR '
                '     p.organisation_id in (SELECT ou.organisation_id '
                '     FROM organisation_user ou WHERE ou.user_id=%s)) '
            )
            query_values = [
                z, x, y,
                z, x, y,
                user.id,
                user.id,
            ]
        return sql, query_values

    def get(self, *args, **kwargs):
        sql, query_values = (
            self.generate_query_for_map(
                self.request.user,
                kwargs.get('z'),
                kwargs.get('x'),
                kwargs.get('y')
            )
        )
        tile = self.generate_tile(sql, query_values)
        if not len(tile):
            raise Http404()
        return HttpResponse(
            tile,
            content_type="application/x-protobuf")


class AerialTile(APIView):
    """Proxy for aerial map."""
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        """Retrieve aerial by x, y, z."""
        # Note: we can cache the tile to storage
        x = kwargs.get('x')
        y = kwargs.get('y')
        z = kwargs.get('z')
        response = requests.get(
            f'http://aerial.openstreetmap.org.za/ngi-aerial/{z}/{x}/{y}.jpg'
        )
        if response.status_code != 200:
            raise Http404()
        return HttpResponse(
            response.content,
            content_type=response.headers['Content-Type'])


class FindParcelByCoord(APIView):
    """Find parcel that contains coordinate."""
    permission_classes = [IsAuthenticated]

    def find_erf(self, point: Point):
        """Find Erf parcel by point."""
        parcel = Erf.objects.filter(geom__contains=point)
        if parcel:
            return ErfParcelSerializer(
                parcel.first()
            ).data
        return None

    def find_holding(self, point: Point):
        """Find Holding parcel by point."""
        parcel = Holding.objects.filter(geom__contains=point)
        if parcel:
            return HoldingParcelSerializer(
                parcel.first()
            ).data
        return None

    def find_farm_portion(self, point: Point):
        """Find FarmPortion parcel by point."""
        parcel = FarmPortion.objects.filter(geom__contains=point)
        if parcel:
            return FarmPortionParcelSerializer(
                parcel.first()
            ).data
        return None

    def find_parent_farm(self, point: Point):
        """Find ParentFarm parcel by point."""
        parcel = ParentFarm.objects.filter(geom__contains=point)
        if parcel:
            return ParentFarmParcelSerializer(
                parcel.first()
            ).data
        return None

    def get(self, *args, **kwargs):
        # Note: we can cache this API
        lat = self.request.GET.get('lat', 0)
        lng = self.request.GET.get('lng', 0)
        point = Point(float(lng), float(lat), srid=4326)
        point.transform(3857)
        # find erf
        parcel = self.find_erf(point)
        if parcel:
            return Response(status=200, data=parcel)
        # find holding
        parcel = self.find_holding(point)
        if parcel:
            return Response(status=200, data=parcel)
        # find farm_portion
        parcel = self.find_farm_portion(point)
        if parcel:
            return Response(status=200, data=parcel)
        # find parent_farm
        parcel = self.find_parent_farm(point)
        if parcel:
            return Response(status=200, data=parcel)
        return Response(status=404)
