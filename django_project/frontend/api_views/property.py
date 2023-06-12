"""API Views related to property."""
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import (
    GEOSGeometry
)
from django.contrib.gis.db.models import Union
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from area import area
from property.models import (
    PropertyType,
    Province,
    Property,
    OwnershipStatus,
    ParcelType,
    Parcel
)
from stakeholder.models import (
    Organisation
)
from frontend.models.parcels import (
    Erf,
    Holding,
    FarmPortion,
    ParentFarm
)
from frontend.serializers.property import (
    PropertyTypeSerializer,
    ProvinceSerializer
)
from frontend.serializers.stakeholder import (
    OrganisationSerializer
)


class CreateNewProperty(APIView):
    """Create new property API."""
    permission_classes = [IsAuthenticated]

    def get_geom_size_in_ha(self, geom: GEOSGeometry):
        meters_sq = area(geom.geojson)
        acres = meters_sq * 0.000247105381 # meters^2 to acres
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
        ownership_status = OwnershipStatus.objects.all().first()
        data = {
            'name': request.data.get('name'),
            'owner_email': request.data.get('owner_email'),
            'property_type_id': request.data.get('property_type_id'),
            'province_id': request.data.get('province_id'),
            'organisation_id': request.data.get('organisation_id'),
            'geometry': geom,
            'area_available': 0,
            'property_size_ha': self.get_geom_size_in_ha(geom) if geom else 0,
            'ownership_status_id': ownership_status.id,
            'created_by_id': self.request.user.id,
            'created_at': datetime.now()
        }
        property = Property.objects.create(**data)
        return Response(status=201, data={
            'id': property.id
        })


class PropertyMetadataList(APIView):
    """Get metadata for property: type, organisation, province."""
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        provinces = Province.objects.all().order_by('name')
        types = PropertyType.objects.all().order_by('name')
        organisations = Organisation.objects.all().order_by('name')
        if not self.request.user.is_superuser:
            # filter by organisation that the user belongs to
            pass
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
