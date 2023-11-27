# -*- coding: utf-8 -*-

"""API Views related to statistical.
"""
import json
import ast
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.http.response import HttpResponse
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
    """
    Fetch trend of species.

    Returns:
        Response: JSON response containing trend data.
    """
    permission_classes = [IsAuthenticated]

    def get_model_output(self, species: Taxon):
        model_output = SpeciesModelOutput.objects.filter(
            taxon=species,
            is_latest=True,
            status=DONE
        ).first()
        if model_output is None:
            return None
        if (
            model_output.output_file and
            model_output.output_file.storage.exists(
                model_output.output_file.name)
        ):
            return model_output
        return None

    def get_properties_names(self):
        filter_property = self.request.data.get('property', None)
        property_id_list = []
        if filter_property:
            property_id_list = ast.literal_eval('(' + filter_property + ',)')
        return Property.objects.filter(
            id__in=property_id_list
        ).values_list('name', flat=True).distinct()

    def get_filtered_properties_trends(self, trends, properties):
        return [trend for trend in trends if trend['property'] in properties]

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
        model_output = self.get_model_output(species)
        if model_output is None:
            return Response(status=200, data=[])
        properties = self.get_properties_names()
        trends = []
        with model_output.output_file.open('r') as json_file:
            json_dict = json.load(json_file)
            if PROPERTY_TREND in json_dict:
                trends = json_dict[PROPERTY_TREND]
        return Response(
            status=200,
            data=self.get_filtered_properties_trends(trends, properties))


class DownloadTrendDataAsJson(SpeciesTrend):
    """Download trend data as json."""

    def post(self, *args, **kwargs):
        species_name = self.request.data.get('species', None)
        species = get_object_or_404(
            Taxon, scientific_name=species_name
        )
        model_output = self.get_model_output(species)
        if model_output is None:
            return Response(status=404, data={
                'detail': 'Empty data model for given species!'
            })
        properties = self.get_properties_names()
        with model_output.output_file.open('r') as json_file:
            json_dict = json.load(json_file)
            if PROPERTY_TREND in json_dict:
                trends = json_dict[PROPERTY_TREND]
                filtered_property_trends = (
                    self.get_filtered_properties_trends(trends, properties)
                )
                json_dict[PROPERTY_TREND] = filtered_property_trends
        response = HttpResponse(content=json.dumps(json_dict))
        response['Content-Type'] = 'application/json'
        response['Content-Disposition'] = (
            f'attachment; filename={species_name}.json'
        )
        return response
