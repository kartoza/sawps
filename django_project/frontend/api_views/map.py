# -*- coding: utf-8 -*-


"""API Views related to map.
"""
from typing import Tuple, List
import requests
import io
import gzip
import datetime
from django.core.cache import cache
from django.db import connection
from django.db.utils import ProgrammingError
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404, HttpResponseForbidden
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.utils import timezone
from property.models import (
    Property,
    Parcel
)
from frontend.models.context_layer import ContextLayer
from frontend.models.map_session import MapSession
from frontend.serializers.context_layer import ContextLayerSerializer
from frontend.utils.map import (
    get_map_template_style,
    generate_population_count_categories,
    generate_map_view,
    MapQueryEnum
)
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
from stakeholder.models import OrganisationUser
from frontend.utils.organisation import get_current_organisation_id
from frontend.utils.user_roles import check_user_has_permission


User = get_user_model()
PROVINCE_LAYER_ZOOMS = (5, 8)
PROPERTIES_LAYER_ZOOMS = (9, 24)
PROPERTIES_POINT_LAYER_ZOOMS = (5, 24)
PARENT_FARM_LAYER_ZOOMS = (9, 11)
PROPERTIES_LAYER = 'properties'
PROPERTIES_POINTS_LAYER = 'properties-points'
PROPERTIES_BOUNDARY_LAYER = 'properties-boundary'


def should_generate_layer(z: int, zoom_configs: Tuple[int, int]) -> bool:
    """Return True if layer should be generated."""
    return z >= zoom_configs[0] and z <= zoom_configs[1]


class MapSessionBase(APIView):
    """Base class for map filter session."""

    def can_view_properties_layer(self):
        return (
            check_user_has_permission(self.request.user,
                                      'Can view properties layer in the map')
        )

    def can_view_province_layer(self):
        return (
            check_user_has_permission(self.request.user,
                                      'Can view province layer in the map')
        )

    def generate_session(self):
        """
        Generate map filter session from POST data.

        Session will have expiry in 6 hours after creation and
        this expiry date is updated when the session filter is changed.
        """
        session_uuid = self.request.GET.get('session', None)
        session = MapSession.objects.filter(uuid=session_uuid).first()
        filter_species = self.get_species_filter()
        if session is None:
            session = MapSession.objects.create(
                user=self.request.user,
                created_date=timezone.now(),
                expired_date=timezone.now() + datetime.timedelta(hours=6)
            )
        session.species = filter_species
        session.expired_date = timezone.now() + datetime.timedelta(hours=6)
        session.save(update_fields=['species', 'expired_date'])
        if self.can_view_properties_layer():
            generate_map_view(
                session, False,
                self.request.data.get('end_year', None),
                self.request.data.get('species', None),
                self.request.data.get('organisation', None),
                self.request.data.get('activity', None),
                self.request.data.get('spatial_filter_values', None),
                self.request.data.get('property', None)
            )
        if self.can_view_province_layer() and filter_species:
            generate_map_view(
                session, True,
                self.request.data.get('end_year', None),
                self.request.data.get('species', None),
                self.request.data.get('organisation', None),
                self.request.data.get('activity', None),
                self.request.data.get('spatial_filter_values', None),
                self.request.data.get('property', None)
            )
        return session

    def get_species_filter(self):
        """Return species filter if any from POST data."""
        return self.request.data.get('species', None)

    def get_current_session_or_404(self):
        """Retrieve map filter session or return 404."""
        session_uuid = self.request.GET.get('session', None)
        session = MapSession.objects.filter(uuid=session_uuid).first()
        if session is None:
            raise Http404()
        return session

    def get_map_query_type(self):
        """Check map query type: default (by active org) or filter session."""
        session_uuid = self.request.GET.get('session', None)
        type = MapQueryEnum.MAP_DEFAULT
        if session_uuid:
            type = MapQueryEnum.MAP_USING_SESSION
        return type


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


class MapStyles(MapSessionBase):
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
        map_query_type = self.get_map_query_type()
        session = None
        if map_query_type == MapQueryEnum.MAP_USING_SESSION:
            session_obj = self.get_current_session_or_404()
            session = str(session_obj.uuid) if session_obj else None
        styles = get_map_template_style(
            self.request,
            session=session,
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


class LayerMVTTilesBase(APIView):
    """Base class for generating dynamic VT."""
    permission_classes = [IsAuthenticated]

    def get_geom_field_for_properties_layers(self, layer_name: str):
        if layer_name == PROPERTIES_POINTS_LAYER:
            return 'centroid'
        if layer_name == PROPERTIES_BOUNDARY_LAYER:
            return 'boundary'
        return 'geometry'

    def gzip_tile(self, data):
        """Apply gzip to vector tiles bytes."""
        bytesbuffer = io.BytesIO()
        with gzip.GzipFile(fileobj=bytesbuffer, mode='w') as w:
            w.write(data)
        return bytesbuffer.getvalue()

    def get_mvt_sql(self, mvt_name, sql):
        """Generate ST_MVT sql for single query."""
        fsql = (
            '(SELECT ST_AsMVT(q,\'{mvt_name}\',4096,\'geom\',\'id\') '
            'AS data '
            'FROM ({query}) AS q)'
        ).format(
            mvt_name=mvt_name,
            query=sql
        )
        return fsql

    def generate_tile(self, sql, query_values):
        """Execute sql to generate vector tile bytes array."""
        if sql is None:
            return []
        try:
            tile = bytes()
            with connection.cursor() as cursor:
                raw_sql = (
                    'SELECT ({sub_sqls}) AS data'
                ).format(sub_sqls=sql)
                cursor.execute(raw_sql, query_values)
                row = cursor.fetchone()
                tile = row[0]
            return tile
        except ProgrammingError:
            return []

    def generate_queries_for_vector_tiles(self):
        raise NotImplementedError()

    def get(self, *args, **kwargs):
        sql, query_values = self.generate_queries_for_vector_tiles()
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


class SessionPropertiesLayerMVTTiles(MapSessionBase, LayerMVTTilesBase):
    """Dynamic Vector Tile for properties layer based on filter session."""
    permission_classes = [IsAuthenticated]

    def get_properties_layer_query(
            self,
            layer_name: str,
            session: MapSession,
            z: int, x: int, y: int) -> Tuple[str, List[str]]:
        """Generate SQL query for properties/points using filter session."""
        geom_field = (
            self.get_geom_field_for_properties_layers(layer_name)
        )
        sql = (
            """
            SELECT p.id, p.name, population_summary.count,
            ST_AsMVTGeom(
              ST_Transform(p.{geom_field}, 3857),
              TileBBox(%s, %s, %s, 3857)) as geom
            from property p
            inner join "{view_name}" population_summary
                on p.id=population_summary.id
            where p.{geom_field} && TileBBox(%s, %s, %s, 4326)
            """
        ).format(
            geom_field=geom_field,
            view_name=session.properties_view_name
        )
        query_values = [
            z, x, y,
            z, x, y
        ]
        return self.get_mvt_sql(layer_name, sql), query_values

    def get_province_layer_query(
            self, session: MapSession,
            z: int, x: int, y: int):
        """Generate SQL query for province layer using filter session."""
        sql = (
            """
            select zpss.id, zpss.adm1_en, population_summary.count,
              ST_AsMVTGeom(zpss.geom, TileBBox(%s, %s, %s, 3857)) as geom
            from layer.zaf_provinces_small_scale zpss
            inner join province p2 on p2.name=zpss.adm1_en
            inner join "{view_name}" population_summary
                on p2.id=population_summary.id
            where zpss.geom && TileBBox(%s, %s, %s, 3857)
            """
        ).format(view_name=session.province_view_name)
        query_values = [z, x, y, z, x, y]
        return self.get_mvt_sql('province_population', sql), query_values

    def generate_queries_for_map_session(
            self,
            session: MapSession,
            z: int, x: int, y: int) -> Tuple[str, List[str]]:
        """
        Generate layer queries for vector tiles using filter session.

        Possible layers: province_population, properties, properties-point.
        """
        sqls = []
        query_values = []
        if (
            self.can_view_province_layer() and session.species and
            should_generate_layer(z, PROVINCE_LAYER_ZOOMS)
        ):
            province_sql, province_val = (
                self.get_province_layer_query(session, z, x, y)
            )
            sqls.append(province_sql)
            query_values.extend(province_val)
        if self.can_view_properties_layer():
            if should_generate_layer(z, PROPERTIES_LAYER_ZOOMS):
                properties_sql, properties_val = (
                    self.get_properties_layer_query(
                        PROPERTIES_LAYER, session, z, x, y)
                )
                sqls.append(properties_sql)
                query_values.extend(properties_val)
                # add properties boundary layer
                prop_boundary_sql, prop_boundary_val = (
                    self.get_properties_layer_query(
                        PROPERTIES_BOUNDARY_LAYER, session, z, x, y)
                )
                sqls.append(prop_boundary_sql)
                query_values.extend(prop_boundary_val)
            if should_generate_layer(z, PROPERTIES_POINT_LAYER_ZOOMS):
                properties_points_sql, properties_points_val = (
                    self.get_properties_layer_query(
                        PROPERTIES_POINTS_LAYER, session, z, x, y)
                )
                sqls.append(properties_points_sql)
                query_values.extend(properties_points_val)
        if len(sqls) == 0:
            return None, None
        # construct output_sql
        output_sql = '||'.join(sqls)
        return output_sql, query_values

    def generate_queries_for_vector_tiles(self):
        session = self.get_current_session_or_404()
        return (
            self.generate_queries_for_map_session(
                session,
                int(self.kwargs.get('z')),
                int(self.kwargs.get('x')),
                int(self.kwargs.get('y'))
            )
        )


class DefaultPropertiesLayerMVTTiles(MapSessionBase, LayerMVTTilesBase):
    """Dynamic Vector Tile for properties layer based on active org."""
    permission_classes = [IsAuthenticated]

    def get_user_organisation_id(self):
        # get active organisation ids
        current_organisation_id = get_current_organisation_id(
            self.request.user
        ) or 0
        return current_organisation_id

    def get_default_properties_layer_query(
            self,
            layer_name: str,
            z: int, x: int, y: int) -> Tuple[str, List[str]]:
        """Generate SQL query for properties/points using active org."""
        geom_field = (
            self.get_geom_field_for_properties_layers(layer_name)
        )
        sql = (
            """
            SELECT p.id, p.name, 0 as count,
            ST_AsMVTGeom(
              ST_Transform(p.{geom_field}, 3857),
              TileBBox(%s, %s, %s, 3857)) as geom
            from property p
            where p.{geom_field} && TileBBox(%s, %s, %s, 4326)
            AND p.organisation_id=%s
            """
        ).format(
            geom_field=geom_field
        )
        query_values = [
            z, x, y,
            z, x, y,
            self.get_user_organisation_id()
        ]
        return self.get_mvt_sql(layer_name, sql), query_values

    def generate_queries_for_map_default(
            self, z: int, x: int, y: int) -> Tuple[str, List[str]]:
        """
        Generate layer queries for vector tile using active organisation.

        Possible layers: properties, properties-point.
        """
        sqls = []
        query_values = []
        if not self.can_view_properties_layer():
            return None, None
        if should_generate_layer(z, PROPERTIES_LAYER_ZOOMS):
            properties_sql, properties_val = (
                self.get_default_properties_layer_query(
                    PROPERTIES_LAYER, z, x, y)
            )
            sqls.append(properties_sql)
            query_values.extend(properties_val)
            prop_boundary_sql, prop_boundary_val = (
                self.get_default_properties_layer_query(
                    PROPERTIES_BOUNDARY_LAYER, z, x, y)
            )
            sqls.append(prop_boundary_sql)
            query_values.extend(prop_boundary_val)
        if should_generate_layer(z, PROPERTIES_POINT_LAYER_ZOOMS):
            properties_points_sql, properties_points_val = (
                self.get_default_properties_layer_query(
                    PROPERTIES_POINTS_LAYER, z, x, y)
            )
            sqls.append(properties_points_sql)
            query_values.extend(properties_points_val)
        if len(sqls) == 0:
            return None, None
        # construct output_sql
        output_sql = '||'.join(sqls)
        return output_sql, query_values

    def generate_queries_for_vector_tiles(self):
        return (
            self.generate_queries_for_map_default(
                int(self.kwargs.get('z')),
                int(self.kwargs.get('x')),
                int(self.kwargs.get('y'))
            )
        )


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

    def find_parcel(self, cls, cls_serializer, point: Point):
        """Find parcel by point."""
        parcel = cls.objects.filter(geom__contains=point)
        if parcel:
            return cls_serializer(
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
        zoom = int(self.request.GET.get('zoom', 12))
        point = Point(float(lng), float(lat), srid=4326)
        point.transform(3857)
        if (
            zoom >= PARENT_FARM_LAYER_ZOOMS[0] and
            zoom <= PARENT_FARM_LAYER_ZOOMS[1]
        ):
            # find parent_farm
            parcel = self.find_parcel(ParentFarm, ParentFarmParcelSerializer,
                                      point)
            if parcel:
                if self.check_used_parcel(parcel['cname'], property_id):
                    return Response(status=404)
                return Response(status=200, data=parcel)
        else:
            map_serializers = {
                Erf: ErfParcelSerializer,
                Holding: HoldingParcelSerializer,
                FarmPortion: FarmPortionParcelSerializer
            }
            for parcel_class, parcel_serializer in map_serializers.items():
                parcel = self.find_parcel(parcel_class,
                                          parcel_serializer, point)
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
        properties = Property.objects.filter(
            geometry__contains=point
        )
        if not self.request.user.is_superuser:
            org_ids = OrganisationUser.objects.filter(
                user=self.request.user
            ).values_list('organisation_id', flat=True).distinct()
            properties = properties.filter(
                organisation_id__in=org_ids
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


class PopulationCountLegends(MapSessionBase):
    """API to iniitalize map session based on user filters."""
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        species = self.get_species_filter()
        session = self.generate_session()
        province = []
        if self.can_view_province_layer() and species:
            province = generate_population_count_categories(
                True, session, species
            )
        properties = []
        if self.can_view_properties_layer() and species:
            properties = generate_population_count_categories(
                False, session, species
            )
        return Response(status=200, data={
            'province': province,
            'properties': properties,
            'session': str(session.uuid)
        })
