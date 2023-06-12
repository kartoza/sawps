"""API Views related to map."""
from typing import Tuple, List
import requests
from django.db import connection
from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from frontend.models.context_layer import ContextLayer
from frontend.serializers.context_layer import ContextLayerSerializer
from frontend.utils.map import get_map_template_style


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
                'SELECT ST_AsMVT(tile.*, '
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
            user,
            z: int,
            x: int,
            y: int,) -> Tuple[str, List[str]]:
        query_values = []
        sql = (
            'SELECT p.id, p.name, '
            'ST_AsMVTGeom('
            '  ST_Transform(p.geometry, 3857), '
            '  TileBBox(%s, %s, %s, 3857)) as geom '
            'from property p '
            'where p.created_by_id=%s'
        )
        return sql, query_values


class AerialTile(APIView):
    """Proxy for aerial map."""
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        """Retrieve aerial by x, y, z."""
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
