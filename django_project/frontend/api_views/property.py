"""API Views related to property.
"""
from datetime import datetime
from itertools import chain
from django.db.models.functions import Concat
from django.db.models import F, Value, CharField
from area import area
from django.contrib.gis.db.models import Union
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from frontend.models.parcels import Erf, FarmPortion, Holding, ParentFarm
from frontend.serializers.property import (
    PropertyDetailSerializer,
    PropertySerializer,
    PropertyTypeSerializer,
    ProvinceSerializer,
    PropertySearchSerializer
)
from frontend.serializers.places import (
    PlaceLargerScaleSearchSerializer,
    PlaceLargestScaleSearchSerializer,
    PlaceMidScaleSearchSerializer,
    PlaceSmallScaleSearchSerializer
)
from frontend.serializers.stakeholder import OrganisationSerializer
from frontend.utils.organisation import get_current_organisation_id
from property.models import (
    Parcel,
    ParcelType,
    Property,
    PropertyType,
    Province
)
from frontend.models.places import (
    PlaceNameSmallScale,
    PlaceNameMidScale,
    PlaceNameLargerScale,
    PlaceNameLargestScale
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from stakeholder.models import Organisation, OrganisationUser


class CreateNewProperty(APIView):
    """Create new property API."""
    permission_classes = [IsAuthenticated]

    def get_geom_size_in_ha(self, geom: GEOSGeometry):
        meters_sq = area(geom.geojson)
        acres = meters_sq * 0.000247105381  # meters^2 to acres
        return acres / 2.471

    def get_geometry(self, parcels):
        geom: GEOSGeometry = None
        erf_parcel_ids = [p['id'] for p in parcels if p['layer'] == 'erf']
        if erf_parcel_ids:
            queryset = Erf.objects.filter(
                id__in=erf_parcel_ids
            )
            queryset = queryset.aggregate(Union('geom'))
            geom = (
                queryset['geom__union'] if geom is None else
                geom.union(queryset['geom__union'])
            )

        holding_parcel_ids = [p['id'] for p in parcels if
                              p['layer'] == 'holding']
        if holding_parcel_ids:
            queryset = Holding.objects.filter(
                id__in=holding_parcel_ids
            )
            queryset = queryset.aggregate(Union('geom'))
            geom = (
                queryset['geom__union'] if geom is None else
                geom.union(queryset['geom__union'])
            )

        farm_portion_parcel_ids = [p['id'] for p in parcels if
                                   p['layer'] == 'farm_portion']
        if farm_portion_parcel_ids:
            queryset = FarmPortion.objects.filter(
                id__in=farm_portion_parcel_ids
            )
            queryset = queryset.aggregate(Union('geom'))
            geom = (
                queryset['geom__union'] if geom is None else
                geom.union(queryset['geom__union'])
            )

        parent_farm_parcel_ids = [p['id'] for p in parcels if
                                  p['layer'] == 'parent_farm']
        if parent_farm_parcel_ids:
            queryset = ParentFarm.objects.filter(
                id__in=parent_farm_parcel_ids
            )
            queryset = queryset.aggregate(Union('geom'))
            geom = (
                queryset['geom__union'] if geom is None else
                geom.union(queryset['geom__union'])
            )
        if isinstance(geom, Polygon):
            # parcels geom is in 3857
            geom = MultiPolygon([geom], srid=3857)
        if geom:
            # transform srid to 4326
            geom.transform(4326)
        return geom

    def add_parcels(self, property, parcels):
        for parcel in parcels:
            type = parcel['type']
            parcel_type = ParcelType.objects.filter(
                name__iexact=type
            ).first()
            if not parcel_type:
                raise ValidationError(f'Invalid parcel_type: {type}')
            data = {
                'sg_number': parcel['cname'],
                'year': datetime.today().date(),
                'property': property,
                'parcel_type_id': parcel_type.id
            }
            Parcel.objects.create(**data)

    def post(self, request, *args, **kwargs):
        # union of parcels
        parcels = request.data.get('parcels')
        geom = self.get_geometry(parcels)
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
        data = {
            'name': request.data.get('name'),
            'owner_email': request.data.get('owner_email'),
            'property_type_id': request.data.get('property_type_id'),
            'province_id': request.data.get('province_id'),
            'organisation_id': request.data.get('organisation_id'),
            'geometry': geom,
            'property_size_ha': self.get_geom_size_in_ha(geom) if geom else 0,
            'created_by_id': self.request.user.id,
            'created_at': datetime.now()
        }
        property = Property.objects.create(**data)
        self.add_parcels(property, parcels)
        return Response(status=201, data=PropertySerializer(property).data)


class PropertyMetadataList(APIView):
    """Get metadata for property: type, organisation, province."""
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        provinces = Province.objects.all().order_by('name')
        types = PropertyType.objects.all().order_by('name')
        current_organisation_id = get_current_organisation_id(
            self.request.user
        ) or 0
        organisations = Organisation.objects.filter(
            id=current_organisation_id
        ).order_by('name')
        return Response(status=200, data={
            'provinces': (
                ProvinceSerializer(provinces, many=True).data
            ),
            'types': (
                PropertyTypeSerializer(types, many=True).data
            ),
            'organisations': (
                OrganisationSerializer(organisations, many=True).data
            ),
            'user_email': self.request.user.email,
            'user_name': (
                f'{self.request.user.first_name} '
                f'{self.request.user.last_name}' if
                self.request.user.first_name else self.request.user.username
            )
        })


class PropertyList(APIView):
    """Get properties that current user owns."""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        current_organisation_id = get_current_organisation_id(
            request.user
        ) or 0
        organisation_id = current_organisation_id

        organisation = request.GET.get("organisation")
        if organisation:
            _organisation = organisation.split(",")
            properties = Property.objects.filter(
                organisation_id__in=(
                    [int(id) for id in _organisation]
                ),
            )
        else:
            properties = Property.objects.filter(
                organisation_id=organisation_id
            ).order_by('name')

        return Response(
            status=200,
            data=PropertySerializer(properties, many=True).data
        )

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return response


class UpdatePropertyInformation(APIView):
    """Update property information."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        property = get_object_or_404(
            Property,
            id=request.data.get('id')
        )
        property.name = request.data.get('name')
        property.property_type = (
            PropertyType.objects.get(id=request.data.get('property_type_id'))
        )
        property.organisation = (
            Organisation.objects.get(id=request.data.get('organisation_id'))
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
        parcels = request.data.get('parcels')
        geom = self.get_geometry(parcels)
        property.geometry = geom
        property.property_size_ha = (
            self.get_geom_size_in_ha(geom) if geom else 0
        )
        property.save()
        # delete existing parcel
        Parcel.objects.filter(property=property).delete()
        self.add_parcels(property, parcels)
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

    def get(self, *args, **kwargs):
        search_text = self.request.GET.get('search_text', '')
        # filter property from current organisation
        current_organisation_id = get_current_organisation_id(
            self.request.user
        ) or 0
        properties = Property.objects.filter(
            name__istartswith=search_text,
            organisation_id=current_organisation_id
        ).order_by('name')[:10]
        properties_search_results = PropertySearchSerializer(
            properties,
            many=True
        ).data
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
