# -*- coding: utf-8 -*-

"""API Views related to statistical.
"""
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from species.models import Taxon
from population_data.models import AnnualPopulation
from frontend.models import StatisticalModel, NATIONAL_TREND
from frontend.utils.statistical_model import (
    execute_statistical_model,
    write_plumber_data,
    remove_plumber_data,
    save_statistical_model_output_cache,
    get_statistical_model_output_cache
)


class SpeciesNationalTrend(APIView):
    """Fetch national trend of species."""
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        species_id = kwargs.get('species_id')
        species = get_object_or_404(Taxon, id=species_id)
        cached_json_data = get_statistical_model_output_cache(
            species, NATIONAL_TREND)
        if cached_json_data:
            return Response(status=200, data=cached_json_data)
        statistical_model = StatisticalModel.objects.filter(
            taxon=species
        ).first()
        csv_headers = [
            'property', 'province', 'species', 'year', 'count_total',
            'survey_method', 'count_method'
        ]
        rows = AnnualPopulation.objects.select_related(
            'owned_species', 'survey_method', 'count_method',
            'owned_species__taxon',
            'owned_species__property', 'owned_species__property__province'
        ).filter(
            owned_species__taxon=species
        ).order_by('year')
        csv_data = [
            [
                row.owned_species.property.name,
                row.owned_species.property.province.name,
                row.owned_species.taxon.scientific_name,
                row.year,
                row.total,
                row.survey_method.name,
                row.count_method.name
            ] for row in rows
        ]
        data_filepath = write_plumber_data(csv_headers, csv_data)
        is_success, json_data = execute_statistical_model(
            data_filepath, model=statistical_model)
        # remove data_filepath
        remove_plumber_data(data_filepath)
        if is_success:
            national_trend_data = json_data.get(NATIONAL_TREND, [])
            save_statistical_model_output_cache(species, NATIONAL_TREND,
                                                national_trend_data)
            return Response(status=200, data=national_trend_data)
        return Response(status=200, data=[])
