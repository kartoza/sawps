"""API Views related to property.
"""
from datetime import datetime
from itertools import chain

from django.contrib.gis.db.models import Union
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon
from django.core.exceptions import ValidationError
from django.db.models import F, Value, CharField, Q
from django.db.models.expressions import RawSQL
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from frontend.models.parcels import Erf, FarmPortion, Holding, ParentFarm
from frontend.models.places import (
    PlaceNameSmallScale,
    PlaceNameMidScale,
    PlaceNameLargerScale,
    PlaceNameLargestScale
)
from frontend.serializers.places import (
    PlaceLargerScaleSearchSerializer,
    PlaceLargestScaleSearchSerializer,
    PlaceMidScaleSearchSerializer,
    PlaceSmallScaleSearchSerializer
)
from frontend.serializers.property import (
    PropertyDetailSerializer,
    PropertySerializer,
    PropertyTypeSerializer,
    PropertySearchSerializer,
    PropertyTypeColourSerializer,
    ProvinceSerializer
)
from frontend.serializers.stakeholder import OrganisationSerializer
from frontend.static_mapping import PROVINCIAL_ROLES
from frontend.utils.organisation import get_current_organisation_id
from frontend.utils.parcel import find_province, get_geom_size_in_ha
from frontend.utils.user_roles import (
    get_user_roles,
    check_user_has_permission
)
from population_data.models import OpenCloseSystem
from population_data.serializers import (
    OpenCloseSystemSerializer,
)
from property.models import (
    Parcel,
    ParcelType,
    Property,
    PropertyType,
    Province,
    BOUNDARY_FILE_SOURCE_TYPE,
    DIGITISE_SOURCE_TYPE,
    SELECT_SOURCE_TYPE
)
from stakeholder.models import Organisation, OrganisationUser
from frontend.models.map_session import MapSession
from frontend.models.boundary_search import BoundarySearchRequest


class CheckPropertyNameIsAvailable(APIView):
    """Validate if property name is available."""
    permission_classes = [IsAuthenticated]

    def validate_property_name(self, name, property_id=None):
        properties = Property.objects.filter(
            name=name
        )
        if property_id:
            properties = properties.exclude(id=property_id)
        return not properties.exists()

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        property_id = request.data.get('id', None)
        return Response(
            status=200,
            data={
                'name': name,
                'available': self.validate_property_name(name, property_id)
            }
        )


class CreateNewProperty(CheckPropertyNameIsAvailable):
    """Create new property API."""
    permission_classes = [IsAuthenticated]

    def check_parcel_ids(self, cls, parcel_ids):
        queryset = cls.objects.filter(
            id__in=parcel_ids
        )
        return queryset.values_list('id', flat=True)

    def group_parcels(self, parcels):
        erf_parcel_ids = []
        holding_parcel_ids = []
        farm_portion_parcel_ids = []
        parent_farm_parcel_ids = []
        cnames = []
        for parcel in parcels:
            if parcel['cname'] in cnames:
                continue
            cnames.append(parcel['cname'])
            if parcel['layer'] == 'erf':
                erf_parcel_ids.append(parcel['id'])
            elif parcel['layer'] == 'holding':
                holding_parcel_ids.append(parcel['id'])
            elif parcel['layer'] == 'farm_portion':
                farm_portion_parcel_ids.append(parcel['id'])
            elif parcel['layer'] == 'parent_farm':
                parent_farm_parcel_ids.append(parcel['id'])
        return {
            'erf': self.check_parcel_ids(Erf, erf_parcel_ids),
            'holding': self.check_parcel_ids(Holding, holding_parcel_ids),
            'farm_portion': self.check_parcel_ids(FarmPortion,
                                                  farm_portion_parcel_ids),
            'parent_farm': self.check_parcel_ids(ParentFarm,
                                                 parent_farm_parcel_ids),
        }

    def find_parcel_geom(self, cls, parcel_ids, geom):
        queryset = cls.objects.filter(
            id__in=parcel_ids
        )
        queryset = queryset.aggregate(Union('geom'))
        other_geom = queryset['geom__union']
        if other_geom:
            geom = (
                other_geom if geom is None else
                geom.union(other_geom)
            )
        return geom

    def get_geometry(self, filtered_ids):
        geom: GEOSGeometry = None
        parcel_cls_map = {
            'erf': Erf,
            'holding': Holding,
            'farm_portion': FarmPortion,
            'parent_farm': ParentFarm
        }
        for layer, parcel_cls in parcel_cls_map.items():
            ids = filtered_ids[layer]
            if ids:
                geom = self.find_parcel_geom(parcel_cls, ids, geom)
        if isinstance(geom, Polygon):
            # parcels geom is in 3857
            geom = MultiPolygon([geom], srid=3857)
        province = find_province(geom, Province.objects.first())
        if geom:
            # transform srid to 4326
            geom.transform(4326)
        return geom, province

    def add_parcels(self, property, parcels, filtered_ids):
        cnames = []
        for parcel in parcels:
            layer = parcel['layer']
            obj_id = parcel['id']
            cname = parcel['cname']
            if cname in cnames:
                continue
            if obj_id not in filtered_ids[layer]:
                continue
            type = parcel['type']
            parcel_type = ParcelType.objects.filter(
                name__iexact=type
            ).first()
            if not parcel_type:
                raise ValidationError(f'Invalid parcel_type: {type}')
            data = {
                'sg_number': cname,
                'year': datetime.today().date(),
                'property': property,
                'parcel_type_id': parcel_type.id,
                'source': layer,
                'source_id': obj_id
            }
            Parcel.objects.create(**data)
            cnames.append(cname)

    def get_property_geom(self, request, boundary_source,
                          boundary_search = None):
        geom = None
        filtered_ids = {}
        province = None
        property_size_ha = 0
        parcels = []
        if boundary_source == BOUNDARY_FILE_SOURCE_TYPE:
            geom = boundary_search.geometry
            province = boundary_search.province
            property_size_ha = boundary_search.property_size_ha
        else:
            # union of parcels
            parcels = request.data.get('parcels')
            filtered_ids = self.group_parcels(parcels)
            geom, province = self.get_geometry(filtered_ids)
            property_size_ha = get_geom_size_in_ha(geom)
        return geom, province, property_size_ha, parcels, filtered_ids

    def save_property_parcels(self, is_update, property,
                              parcels, filtered_ids):
        if is_update:
            # delete existing parcel
            Parcel.objects.filter(property=property).delete()
        self.add_parcels(property, parcels, filtered_ids)

    def find_boundary_search_session(self):
        boundary_source = SELECT_SOURCE_TYPE
        boundary_search = None
        boundary_search_session = self.request.data.get(
            'boundary_search_session', None)
        if boundary_search_session:
            boundary_search = BoundarySearchRequest.objects.filter(
                session=boundary_search_session
            ).first()
            if boundary_search is None:
                return None, None
            if boundary_search.type == 'File':
                # uploaded file
                boundary_source = BOUNDARY_FILE_SOURCE_TYPE
            else:
                # digitise
                boundary_source = DIGITISE_SOURCE_TYPE
        return boundary_source, boundary_search

    def post(self, request, *args, **kwargs):
        current_organisation_id = get_current_organisation_id(
            request.user
        ) or 0
        organisation_id = current_organisation_id
        if not organisation_id:
            return Response(status=400, data='Invalid Organisation!')
        # validate if user belongs to the organisation
        if not self.request.user.is_superuser:
            organisation_user = OrganisationUser.objects.filter(
                organisation_id=organisation_id,
                user=self.request.user
            )
            if not organisation_user.exists():
                return Response(
                    status=403,
                    data='User does not belong to this organisation!'
                )
        property_name = request.data.get('name')
        if not self.validate_property_name(property_name):
            return Response(
                status=400, data=(
                    f'There is existing property with name {property_name}! '
                    'Please use other name for the property!'
                ))
        boundary_source, boundary_search = self.find_boundary_search_session()
        if boundary_source is None and boundary_search is None:
            return Response(
                status=400, data=(
                    'Invalid property session! '
                    'Please try again or contact administrator!'
                ))
        geom, province, property_size_ha, parcels, filtered_ids = (
            self.get_property_geom(request, boundary_source, boundary_search)
        )
        if not province:
            return Response(
                status=400, data=(
                    'Invalid Province! Please contact administrator '
                    'to populate province table!'
                ))
        data = {
            'name': property_name,
            'owner_email': request.data.get('owner_email'),
            'property_type_id': request.data.get('property_type_id'),
            'province_id': province.id,
            'open_id': request.data.get('open_id'),
            'organisation_id': request.data.get('organisation_id'),
            'geometry': geom,
            'property_size_ha': property_size_ha,
            'created_by_id': self.request.user.id,
            'created_at': datetime.now(),
            'centroid': geom.point_on_surface,
            'boundary_source': boundary_source
        }
        property = Property.objects.create(**data)

        if boundary_source != BOUNDARY_FILE_SOURCE_TYPE:
            # Selection and digitise will have parcels
            try:
                self.save_property_parcels(False, property,
                                           parcels, filtered_ids)
            except ValidationError as e:
                return Response(status=400, data=e.message)
        return Response(status=201, data=PropertySerializer(property).data)


class PropertyMetadataList(APIView):
    """Get metadata for property: type, organisation, province."""
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        types = PropertyType.objects.all().order_by('name')
        current_organisation_id = get_current_organisation_id(
            self.request.user
        ) or 0
        organisations = Organisation.objects.filter(
            id=current_organisation_id
        ).order_by('name')
        open_close_systems = OpenCloseSystem.objects.all().order_by("name")
        return Response(status=200, data={
            'types': (
                PropertyTypeSerializer(types, many=True).data
            ),
            'organisations': (
                OrganisationSerializer(organisations, many=True).data
            ),
            "opens": (
                OpenCloseSystemSerializer(
                    open_close_systems, many=True).data
            ),
            'user_email': self.request.user.email,
            'user_name': (
                f'{self.request.user.first_name} '
                f'{self.request.user.last_name}' if
                self.request.user.first_name else self.request.user.username
            )
        })


class PropertyList(APIView):
    """Get properties that the current user owns."""
    permission_classes = [IsAuthenticated]

    def get(self, request, organisation_id=None, *args, **kwargs):
        current_organisation_id = get_current_organisation_id(
            request.user
        ) or 0

        if organisation_id:
            # Fetch properties based on
            # the organisation ID provided in the URL
            properties = Property.objects.filter(
                organisation_id=organisation_id
            ).order_by('name')
        else:
            # Fetch properties based on
            # the current organisation set on the user profile
            organisation_id = current_organisation_id

            organisation = request.GET.get("organisation")
            if organisation:
                _organisation = organisation.split(",")
                properties = Property.objects.filter(
                    organisation_id__in=(
                        [int(oid) for oid in _organisation]
                    ),
                ).order_by("name")
            else:
                properties = Property.objects.filter(
                    organisation_id=organisation_id
                ).order_by('name')

        # If role is PROVINCIAL_ROLES and not a super user,
        # limit properties by current organisation province
        # If role is NATIONAL_ROLES/Manager/Member and not a super user,
        # do not filter properties
        if not self.request.user.is_superuser:
            user_roles = set(get_user_roles(self.request.user))
            if user_roles & PROVINCIAL_ROLES:
                if current_organisation_id:
                    current_organisation = Organisation.objects.get(
                        id=current_organisation_id)
                    if current_organisation.province:
                        properties = properties.filter(
                            province=current_organisation.province
                        ).order_by('name')
                    else:
                        properties = Property.objects.none()
                else:
                    properties = Property.objects.none()
        return Response(
            status=200,
            data=PropertySerializer(properties, many=True).data
        )

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return response


class UpdatePropertyInformation(CheckPropertyNameIsAvailable):
    """Update property information."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        property = get_object_or_404(
            Property,
            id=request.data.get('id')
        )
        property_name = request.data.get('name')
        if not self.validate_property_name(property_name, property.id):
            return Response(
                status=400, data=(
                    f'There is existing property with name {property_name}! '
                    'Please use other name for the property!'
                ))
        property.name = property_name
        property.property_type = (
            PropertyType.objects.get(id=request.data.get('property_type_id'))
        )
        property.organisation = (
            Organisation.objects.get(id=request.data.get('organisation_id'))
        )
        property.open = (
            OpenCloseSystem.objects.get(id=request.data.get('open_id'))
        )
        property.save()
        return Response(status=204)


class UpdatePropertyBoundaries(CreateNewProperty):
    """Update property parcels."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        property = get_object_or_404(
            Property,
            id=request.data.get('id')
        )
        boundary_source, boundary_search = self.find_boundary_search_session()
        if boundary_source is None and boundary_search is None:
            return Response(
                status=400, data=(
                    'Invalid property session! '
                    'Please try again or contact administrator!'
                ))
        geom, province, property_size_ha, parcels, filtered_ids = (
            self.get_property_geom(request, boundary_source, boundary_search)
        )
        if not province:
            return Response(
                status=400, data=(
                    'Invalid Province! Please contact administrator '
                    'to populate province table!'
                ))
        property.geometry = geom
        property.property_size_ha = property_size_ha
        property.centroid = geom.point_on_surface
        property.province = province
        property.boundary_source = boundary_source
        property.save()
        if boundary_source != BOUNDARY_FILE_SOURCE_TYPE:
            # Selection and digitise will have parcels
            try:
                self.save_property_parcels(True, property,
                                           parcels, filtered_ids)
            except ValidationError as e:
                return Response(status=400, data=e.message)
        return Response(status=201, data=PropertySerializer(property).data)


class PropertyDetail(APIView):
    """Fetch property detail."""
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        property = get_object_or_404(
            Property,
            id=kwargs.get('id')
        )
        return Response(
            status=200,
            data=PropertyDetailSerializer(property).data
        )


class PropertySearch(APIView):
    """Search property and roads."""
    permission_classes = [IsAuthenticated]
    place_serializers = {
        PlaceNameSmallScale: PlaceSmallScaleSearchSerializer,
        PlaceNameMidScale: PlaceMidScaleSearchSerializer,
        PlaceNameLargerScale: PlaceLargerScaleSearchSerializer,
        PlaceNameLargestScale: PlaceLargestScaleSearchSerializer
    }

    def can_view_properties_layer(self):
        return (
            check_user_has_permission(self.request.user,
                                      'Can view properties layer in the map')
        )

    def search_place(self, cls, serializer_cls, search_text, name_list):
        places = cls.objects.annotate(
            name_type=Concat(F('name'), Value('-'), F('fclass'),
                             output_field=CharField())
        ).filter(
            name__istartswith=search_text
        ).exclude(
            name_type__in=name_list
        ).order_by('name')[:5]
        results = serializer_cls(places, many=True).data
        return results, [f'{p["name"]}-{p["fclass"]}' for p in results]

    def search_property(self, search_text):
        if not self.can_view_properties_layer():
            return []
        session_uuid = self.request.GET.get('session', None)
        session = None
        if session_uuid:
            session = MapSession.objects.filter(uuid=session_uuid).first()
        properties = Property.objects.filter(
            Q(name__istartswith=search_text) |
            Q(short_code__istartswith=search_text)
        )
        if session:
            raw_sql = (
                'SELECT id from "{}"'
            ).format(session.properties_view_name)
            properties = properties.filter(
                id__in=RawSQL(raw_sql, [])
            )
        else:
            # filter property from current organisation
            current_organisation_id = get_current_organisation_id(
                self.request.user
            ) or 0
            properties = properties.filter(
                organisation_id=current_organisation_id
            )
        properties = properties.order_by('name')[:10]
        return PropertySearchSerializer(
            properties,
            many=True
        ).data

    def get(self, *args, **kwargs):
        search_text = self.request.GET.get('search_text', '')
        properties_search_results = self.search_property(search_text)
        place_results = []
        name_list = []
        for place_class, place_serializer in self.place_serializers.items():
            result, names = self.search_place(
                place_class,
                place_serializer,
                search_text,
                name_list
            )
            if names:
                name_list.extend(names)
            place_results.extend(result)
        results = list(chain(properties_search_results, place_results))
        results.sort(key=lambda x: x['name'])
        return Response(
            status=200,
            data=results
        )


class ListPropertyTypeAPIView(APIView):
    """
    API to list Property Type
    """

    def get(self, request):
        properties = PropertyType.objects.order_by('name')
        properties = PropertyTypeColourSerializer(
            properties, many=True
        ).data
        return Response(properties)


class ListProvince(APIView):
    """
    API to list Property Type
    """

    def get(self, request):
        provinces = Province.objects.order_by('name')
        provinces = ProvinceSerializer(
            provinces, many=True
        ).data
        return Response(provinces)
