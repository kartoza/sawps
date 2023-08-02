# -*- coding: utf-8 -*-

"""API Views related to statistical.
"""
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from species.models import Taxon
from population_data.models import AnnualPopulation
from frontend.models import StatisticalModel, NATIONAL_TREND
from frontend.utils.statistical_model import (
    execute_statistical_model,
    write_plumber_data
)


class SpeciesNationalTrend(APIView):
    """Fetch national trend of species."""
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        species_id = kwargs.get('species_id')
        species = get_object_or_404(Taxon, id=species_id)
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
        if is_success:
            return Response(status=200, data=json_data.get(NATIONAL_TREND, []))
        return Response(status=200, data=[])
