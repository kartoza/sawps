# -*- coding: utf-8 -*-


"""API Views related to map.
"""
from typing import Tuple, List
import requests
import io
import gzip
from django.core.cache import cache
from django.db import connection
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404, HttpResponseForbidden
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from property.models import (
    Property,
    Parcel
)
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
from frontend.serializers.property import (
    PropertySerializer
)
from frontend.utils.organisation import (
    get_current_organisation_id
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

    def get_token_for_map(self):
        token = self.request.session.session_key
        expiry_in_seconds = self.request.session.get_expiry_age()
        cache_key = f'map-auth-{token}'
        cache.set(cache_key, True, expiry_in_seconds)
        return token

    def get(self, *args, **kwargs):
        """Retrieve map styles."""
        theme = self.request.GET.get('theme', 'light')
        styles = get_map_template_style(
            self.request,
            theme_choice=(
                0 if theme == 'light' else 1
            ),
            token=self.get_token_for_map()
        )
        return Response(
            status=200,
            data=styles,
            content_type="application/json"
        )


class PropertiesLayerMVTTiles(APIView):
    """Dynamic Vector Tile for properties layer."""
    permission_classes = [IsAuthenticated]

    def gzip_tile(self, data):
        bytesbuffer = io.BytesIO()
        with gzip.GzipFile(fileobj=bytesbuffer, mode='w') as w:
            w.write(data)
        return bytesbuffer.getvalue()

    def generate_tile(self, sql, query_values):
        tile = bytes()
        with connection.cursor() as cursor:
            raw_sql = (
                'SELECT ({sub_sqls}) AS data'
            ).format(sub_sqls=sql)
            cursor.execute(raw_sql, query_values)
            row = cursor.fetchone()
            tile = row[0]
        return tile

    def generate_properties_layer(
            self,
            organisation_id: int,
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
        # add filter by selected organisation
        sql = (
            sql +
            'AND p.organisation_id=%s '
        )
        fsql = (
            '(SELECT ST_AsMVT(q,\'{mvt_name}\',4096,\'geom\',\'id\') '
            'AS data '
            'FROM ({query}) AS q)'
        ).format(
            mvt_name='properties',
            query=sql
        )
        query_values = [
            z, x, y,
            z, x, y,
            organisation_id
        ]
        return fsql, query_values

    def generate_query_for_map(
            self,
            organisation_id: int,
            z: int,
            x: int,
            y: int,) -> Tuple[str, List[str]]:
        sqls = []
        query_values = []
        # generate properties layer
        properties_sql, properties_val = self.generate_properties_layer(
            organisation_id, z, x, y
        )
        sqls.append(properties_sql)
        query_values.extend(properties_val)
        # construct output_sql
        output_sql = '||'.join(sqls)
        return output_sql, query_values

    def get(self, *args, **kwargs):
        current_organisation_id = get_current_organisation_id(
            self.request.user
        ) or 0
        sql, query_values = (
            self.generate_query_for_map(
                current_organisation_id,
                kwargs.get('z'),
                kwargs.get('x'),
                kwargs.get('y')
            )
        )
        tile = self.generate_tile(sql, query_values)
        if not len(tile):
            raise Http404()
        tile_bytes = self.gzip_tile(tile)
        response = HttpResponse(
            tile_bytes,
            status=200,
            content_type='application/vnd.mapbox-vector-tile'
        )
        response['Content-Encoding'] = 'gzip'
        response['Content-Length'] = len(tile_bytes)
        y = kwargs.get('y')
        response['Content-Disposition'] = (
            f'attachment; filename={y}.pbf'
        )
        return response


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

    def check_used_parcel(self, cname: str, existing_property_id: int):
        parcels = Parcel.objects.filter(sg_number=cname)
        if existing_property_id:
            parcels = parcels.exclude(property_id=existing_property_id)
        return parcels.exists()

    def get(self, *args, **kwargs):
        lat = self.request.GET.get('lat', 0)
        lng = self.request.GET.get('lng', 0)
        property_id = self.request.GET.get('property_id', 0)
        point = Point(float(lng), float(lat), srid=4326)
        point.transform(3857)
        # find erf
        parcel = self.find_erf(point)
        if parcel:
            if self.check_used_parcel(parcel['cname'], property_id):
                return Response(status=404)
            return Response(status=200, data=parcel)
        # find holding
        parcel = self.find_holding(point)
        if parcel:
            if self.check_used_parcel(parcel['cname'], property_id):
                return Response(status=404)
            return Response(status=200, data=parcel)
        # find farm_portion
        parcel = self.find_farm_portion(point)
        if parcel:
            if self.check_used_parcel(parcel['cname'], property_id):
                return Response(status=404)
            return Response(status=200, data=parcel)
        # find parent_farm
        parcel = self.find_parent_farm(point)
        if parcel:
            if self.check_used_parcel(parcel['cname'], property_id):
                return Response(status=404)
            return Response(status=200, data=parcel)
        return Response(status=404)


class FindPropertyByCoord(APIView):
    """Find property that contains coordinate."""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lat = self.request.GET.get('lat', 0)
        lng = self.request.GET.get('lng', 0)
        point = Point(float(lng), float(lat), srid=4326)
        current_organisation_id = get_current_organisation_id(
            request.user
        )
        properties = Property.objects.filter(
            geometry__contains=point
        ).filter(
            organisation_id=current_organisation_id
        )
        property = properties.order_by('id').first()
        if not property:
            return Response(status=404)
        return Response(status=200, data=PropertySerializer(property).data)

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return response


class MapAuthenticate(APIView):
    """Check against the token of user."""
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        """Return success 200, so nginx can cache the auth result."""
        token = self.request.query_params.get("token", None)
        if token is None:
            return HttpResponseForbidden()
        cache_key = f'map-auth-{token}'
        allowed = cache.get(cache_key)
        if allowed is not None:
            if allowed:
                return HttpResponse('OK')
        return HttpResponseForbidden()
