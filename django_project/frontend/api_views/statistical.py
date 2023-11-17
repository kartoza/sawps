# -*- coding: utf-8 -*-

"""API Views related to statistical.
"""
import json
import ast
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from frontend.models.base_task import DONE
from species.models import Taxon
from property.models import Property
from frontend.models import (
    SpeciesModelOutput,
    NATIONAL_TREND,
    PROVINCE_TREND,
    NATIONAL_GROWTH,
    PROPERTY_TREND,
    PROVINCIAL_GROWTH
)


class SpeciesNationalTrend(APIView):
    """Fetch national trend of species."""
    permission_classes = [AllowAny]

    def get_trend_data_from_cache(self, species: Taxon,
                                  output_type = NATIONAL_TREND):
        # get latest species model output
        model_output = SpeciesModelOutput.objects.filter(
            taxon=species,
            is_latest=True,
            status=DONE
        ).first()
        if model_output:
            cache_key = model_output.get_cache_key(output_type)
            cached_data = cache.get(cache_key)
            if cached_data:
                return cached_data
        return []

    def get(self, *args, **kwargs):
        species_id = kwargs.get('species_id')
        species = get_object_or_404(Taxon, id=species_id)
        return Response(
            status=200, data=self.get_trend_data_from_cache(species))


class SpeciesTrend(SpeciesNationalTrend):
    """Fetch trend of species based on specified criteria.

    This view allows users to retrieve national trend
    data for a specific species.

    Args:
        request: The HTTP request object containing query parameters.

    Returns:
        Response: JSON response containing trend data.

    """
    permission_classes = [AllowAny]

    def get(self, request):
        species_name = request.GET.get("species")
        level = request.GET.get('level')
        type = request.GET.get('data_type', 'trend')
        species = get_object_or_404(
            Taxon, scientific_name=species_name
        )
        output_type = NATIONAL_TREND
        if type == 'trend':
            if level == 'provincial':
                output_type = PROVINCE_TREND
        elif type == 'growth':
            output_type = NATIONAL_GROWTH
            if level == 'provincial':
                output_type = PROVINCIAL_GROWTH
        else:
            return Response(
                status=400,
                data={
                    'detail': (
                        f'Invalid type: {type}. '
                        'Please use either trend or growth!'
                    )
                }
            )
        return Response(
            status=200,
            data=self.get_trend_data_from_cache(species, output_type))

    def post(self, *args, **kwargs):
        species_name = self.request.data.get('species', None)
        species = get_object_or_404(
            Taxon, scientific_name=species_name
        )
        model_output = SpeciesModelOutput.objects.filter(
            taxon=species,
            is_latest=True,
            status=DONE
        ).first()
        if model_output is None:
            return Response(status=200, data=[])
        if (
            model_output.output_file is None or
            not model_output.output_file.storage.exists(
                model_output.output_file.name)
        ):
            return Response(status=200, data=[])
        filter_property = self.request.data.get('property', None)
        property_id_list = ast.literal_eval('(' + filter_property + ',)')
        properties = Property.objects.filter(
            id__in=property_id_list
        ).values_list('name', flat=True).distinct()
        trends = []
        with model_output.output_file.open('r') as json_file:
            json_dict = json.load(json_file)
            if PROPERTY_TREND in json_dict:
                trends = json_dict[PROPERTY_TREND]
        return Response(status=200, data=[trend for trend in trends if trend['property'] in properties])
