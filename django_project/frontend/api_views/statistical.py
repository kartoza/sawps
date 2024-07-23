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
    PROVINCIAL_GROWTH,
    CUSTOM_AREA_AVAILABLE_GROWTH,
    NUM_PROPERTIES_PER_POP_SIZE_CAT,
    NUM_PROPERTIES_PER_DENSITY_CAT,
    NATIONAL_GROWTH_CAT
)
from frontend.utils.user_roles import check_user_has_permission
from frontend.utils.statistical_model import store_species_model_output_cache


class SpeciesNationalTrend(APIView):
    """Fetch national trend of species."""
    permission_classes = [AllowAny]

    def get_species_model_output(self, species: Taxon,
                                 file_should_exists = False):
        model_output = SpeciesModelOutput.objects.filter(
            taxon=species,
            is_latest=True,
            status=DONE
        ).first()
        if model_output is None:
            return None
        if not file_should_exists:
            return model_output
        if (
            model_output.output_file and
            model_output.output_file.storage.exists(
                model_output.output_file.name)
        ):
            return model_output
        return None

    def get_trend_data_by_type(self, model_output: SpeciesModelOutput,
                               output_type = NATIONAL_TREND):
        results = {
            'metadata': {},
            'results': []
        }
        if model_output is None:
            return results
        # try getting from cache
        cache_key = model_output.get_cache_key(output_type)
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        # fetch from json file and store into cache
        if not (
            model_output.output_file and
            model_output.output_file.storage.exists(
                model_output.output_file.name)
        ):
            return results
        with model_output.output_file.open('r') as json_file:
            json_dict = json.load(json_file)
            store_species_model_output_cache(model_output, json_dict)
            if output_type in json_dict:
                results['results'] = json_dict[output_type]
            if 'metadata' in json_dict:
                results['metadata'] = json_dict['metadata'].get(
                    output_type, {})
        return results

    def get(self, *args, **kwargs):
        species_id = kwargs.get('species_id')
        species = get_object_or_404(Taxon, id=species_id)
        model_output = self.get_species_model_output(species)
        data = self.get_trend_data_by_type(model_output)
        return Response(
            status=200, data=data)


class SpeciesTrend(SpeciesNationalTrend):
    """
    Fetch trend of species.

    Returns:
        Response: JSON response containing trend data.
    """
    permission_classes = [IsAuthenticated]

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

    def can_view_properties_trends(self):
        return (
            check_user_has_permission(self.request.user,
                                      'Can view properties trends data')
        )

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
        elif type == 'area_available_growth':
            output_type = CUSTOM_AREA_AVAILABLE_GROWTH
        elif (
            type in [
                NUM_PROPERTIES_PER_DENSITY_CAT,
                NUM_PROPERTIES_PER_POP_SIZE_CAT
            ]
        ):
            output_type = type
        elif type == 'growth_overall':
            output_type = NATIONAL_GROWTH_CAT
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
        model_output = self.get_species_model_output(species)
        data = self.get_trend_data_by_type(model_output, output_type)
        return Response(
            status=200,
            data=data)

    def post(self, *args, **kwargs):
        if not self.can_view_properties_trends():
            return Response(
                status=403,
                data='User is not allowed to view properties trends data!'
            )
        species_name = self.request.data.get('species', None)
        species = get_object_or_404(
            Taxon, scientific_name=species_name
        )
        model_output = self.get_species_model_output(
            species, file_should_exists=True)
        if model_output is None:
            return Response(status=200, data={
                'metadata': {},
                'results': []
            })
        properties = self.get_properties_names()
        trends = []
        with model_output.output_file.open('r') as json_file:
            json_dict = json.load(json_file)
            if PROPERTY_TREND in json_dict:
                trends = json_dict[PROPERTY_TREND]
        return Response(
            status=200,
            data={
                'metadata': {},
                'results': (
                    self.get_filtered_properties_trends(trends, properties)
                )
            })


class DownloadTrendDataAsJson(SpeciesTrend):
    """Download trend data as json."""

    def post(self, *args, **kwargs):
        species_name = self.request.data.get('species', None)
        species = get_object_or_404(
            Taxon, scientific_name=species_name
        )
        model_output = self.get_species_model_output(
            species, file_should_exists=True)
        if model_output is None:
            return Response(status=404, data={
                'detail': 'Empty data model for given species!'
            })
        with model_output.output_file.open('r') as json_file:
            json_dict = json.load(json_file)
        if self.can_view_properties_trends():
            properties = self.get_properties_names()
            if PROPERTY_TREND in json_dict:
                trends = json_dict[PROPERTY_TREND]
                filtered_property_trends = (
                    self.get_filtered_properties_trends(trends, properties)
                )
                json_dict[PROPERTY_TREND] = filtered_property_trends
        elif PROPERTY_TREND in json_dict:
            del json_dict[PROPERTY_TREND]
        response = HttpResponse(content=json.dumps(json_dict))
        response['Content-Type'] = 'application/json'
        response['Content-Disposition'] = (
            f'attachment; filename={species_name}.json'
        )
        return response
