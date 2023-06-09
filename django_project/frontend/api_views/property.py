"""API Views related to property."""
from datetime import datetime
from django.contrib.gis.geos import (
    GEOSGeometry
)
from django.contrib.gis.db.models import Union
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from frontend.models.parcels import (
    Erf,
    Holding,
    FarmPortion,
    ParentFarm
)
from area import area


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
            data = {
                'sg_number': parcel['cname'],
                'year': datetime.today().year,
                'property': property,
                'parcel_type_id': 0
            }

    def post(self, request, *args, **kwargs):    
        # union of parcels
        parcels = request.data.get('parcels')
        geom = self.get_geometry(parcels)
        data = {
            'name': request.data.get('name'),
            'owner_email': request.data.get('owner_email'),
            'property_type_id': request.data.get('property_type_id'),
            'province_id': request.data.get('province_id'),
            'organisation_id': request.data.get('organisation_id'),
            'geometry': geom,
            'property_size_ha': self.get_geom_size_in_ha(geom) if geom else 0
        }
        new_property_id = 0
        return Response(status=201, data={
            'id': new_property_id
        })
