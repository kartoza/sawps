# -*- coding: utf-8 -*-

"""API Views related to statistical.
"""
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from species.models import Taxon
from population_data.models import AnnualPopulation
from frontend.models import (
    NATIONAL_TREND,
    StatisticalModelOutput
)
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
        statistical_model_output = StatisticalModelOutput.objects.filter(
            model__taxon=species,
            type=NATIONAL_TREND
        ).first()
        csv_headers = [
            'property', 'province', 'species', 'year', 'count_total',
            'survey_method', 'count_method', 'open_closed', 'property_type',
            'property_size', 'area_available_to_species'
        ]
        rows = AnnualPopulation.objects.select_related(
            'owned_species', 'survey_method', 'count_method',
            'owned_species__taxon',
            'owned_species__property', 'owned_species__property__province',
            'owned_species__property__property_type'
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
                row.count_method.name if row.count_method else '',
                'Open' if row.owned_species.property.open else 'Closed',
                row.owned_species.property.property_type.name,
                row.owned_species.property.property_size_ha,
                row.owned_species.area_available_to_species
            ] for row in rows
        ]
        data_filepath = write_plumber_data(csv_headers, csv_data)
        statistical_model = (
            statistical_model_output.model if
            statistical_model_output else None
        )
        is_success, json_data = execute_statistical_model(
            data_filepath, species, model=statistical_model)
        # remove data_filepath
        remove_plumber_data(data_filepath)
        if is_success:
            national_trend_data = json_data.get(NATIONAL_TREND, [])
            save_statistical_model_output_cache(species, NATIONAL_TREND,
                                                national_trend_data)
            return Response(status=200, data=national_trend_data)
        return Response(status=200, data=[])
