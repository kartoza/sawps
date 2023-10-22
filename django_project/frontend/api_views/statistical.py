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
    SPECIES_PER_PROPERTY,
    StatisticalModelOutput
)
from frontend.utils.statistical_model import (
    execute_statistical_model,
    write_plumber_data,
    remove_plumber_data,
    save_statistical_model_output_cache,
    get_statistical_model_output_cache
)
from django.db.models import Q
from frontend.serializers.metrics import AnnualPopulationSerializer


class SpeciesNationalTrend(APIView):
    """Fetch national trend of species."""
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        response = [
            {
                "year": 2019,
                "fit": 345,
                "se.fit": 0.0248,
                "lower_ci": 344.9255,
                "upper_ci": 345.0744
            },
            {
                "year": 2019.5,
                "fit": 343.0886,
                "se.fit": 0.0222,
                "lower_ci": 343.0221,
                "upper_ci": 343.1551
            },
            {
                "year": 2020,
                "fit": 341.3335,
                "se.fit": 0.0251,
                "lower_ci": 341.2581,
                "upper_ci": 341.4088
            },
            {
                "year": 2020.5,
                "fit": 339.8908,
                "se.fit": 0.0297,
                "lower_ci": 339.8016,
                "upper_ci": 339.98
            },
            {
                "year": 2021,
                "fit": 338.9169,
                "se.fit": 0.0324,
                "lower_ci": 338.8197,
                "upper_ci": 339.0141
            },
            {
                "year": 2021.5,
                "fit": 338.5679,
                "se.fit": 0.031,
                "lower_ci": 338.4749,
                "upper_ci": 338.661
            },
            {
                "year": 2022,
                "fit": 339.0002,
                "se.fit": 0.0248,
                "lower_ci": 338.9257,
                "upper_ci": 339.0746
            },
            {
                "year": 2022.5,
                "fit": 340.2657,
                "se.fit": 0.0179,
                "lower_ci": 340.2119,
                "upper_ci": 340.3194
            },
            {
                "year": 2023,
                "fit": 341.9999,
                "se.fit": 0.0248,
                "lower_ci": 341.9254,
                "upper_ci": 342.0743
            }
        ]
        # species_id = kwargs.get('species_id')
        # species = get_object_or_404(Taxon, id=species_id)
        # cached_json_data = get_statistical_model_output_cache(
        #     species, NATIONAL_TREND)
        # if cached_json_data:
        #     return Response(status=200, data=cached_json_data)
        # statistical_model_output = StatisticalModelOutput.objects.filter(
        #     model__taxon=species,
        #     type=NATIONAL_TREND
        # ).first()
        # csv_headers = [
        #     'property', 'province', 'species', 'year', 'count_total',
        #     'survey_method', 'open_closed', 'property_type',
        #     'property_size', 'area_available_to_species'
        # ]
        # rows = AnnualPopulation.objects.select_related(
        #     'owned_species', 'survey_method',
        #     'owned_species__taxon',
        #     'owned_species__property', 'owned_species__property__province',
        #     'owned_species__property__property_type'
        # ).filter(
        #     owned_species__taxon=species
        # ).order_by('year')
        # csv_data = [
        #     [
        #         row.owned_species.property.name,
        #         row.owned_species.property.province.name,
        #         row.owned_species.taxon.scientific_name,
        #         row.year,
        #         row.total,
        #         row.survey_method.name if row.survey_method else '',
        #         'Open' if row.owned_species.property.open else 'Closed',
        #         row.owned_species.property.property_type.name,
        #         row.owned_species.property.property_size_ha,
        #         row.owned_species.area_available_to_species
        #     ] for row in rows
        # ]
        # data_filepath = write_plumber_data(csv_headers, csv_data)
        # statistical_model = (
        #     statistical_model_output.model if
        #     statistical_model_output else None
        # )
        # is_success, json_data = execute_statistical_model(
        #     data_filepath, species, model=statistical_model)
        # # remove data_filepath
        # remove_plumber_data(data_filepath)
        # if is_success:
        #     national_trend_data = json_data.get(NATIONAL_TREND, [])
        #     save_statistical_model_output_cache(species, NATIONAL_TREND,
        #                                         national_trend_data)
        #     return Response(status=200, data=national_trend_data)
        # return Response(status=200, data=[])
        return Response(status=200, data=response)


class SpeciesTrend(APIView):
    """Fetch trend of species based on specified criteria.

    This view allows users to retrieve national trend
    data for a specific species while filtering by properties,
    start and end years. The view first attempts to fetch
    cached data, and if not found, retrieves data from the database.
    The retrieved data is then processed to generate
    statistical model output.

    Args:
        request: The HTTP request object containing query parameters.

    Returns:
        Response: JSON response containing trend data.

    """
    permission_classes = [AllowAny]

    def get(self, request):
        response =         response = [
            {
                "year": 2019,
                "fit": 345,
                "se.fit": 0.0248,
                "lower_ci": 344.9255,
                "upper_ci": 345.0744
            },
            {
                "year": 2019.5,
                "fit": 343.0886,
                "se.fit": 0.0222,
                "lower_ci": 343.0221,
                "upper_ci": 343.1551
            },
            {
                "year": 2020,
                "fit": 341.3335,
                "se.fit": 0.0251,
                "lower_ci": 341.2581,
                "upper_ci": 341.4088
            },
            {
                "year": 2020.5,
                "fit": 339.8908,
                "se.fit": 0.0297,
                "lower_ci": 339.8016,
                "upper_ci": 339.98
            },
            {
                "year": 2021,
                "fit": 338.9169,
                "se.fit": 0.0324,
                "lower_ci": 338.8197,
                "upper_ci": 339.0141
            },
            {
                "year": 2021.5,
                "fit": 338.5679,
                "se.fit": 0.031,
                "lower_ci": 338.4749,
                "upper_ci": 338.661
            },
            {
                "year": 2022,
                "fit": 339.0002,
                "se.fit": 0.0248,
                "lower_ci": 338.9257,
                "upper_ci": 339.0746
            },
            {
                "year": 2022.5,
                "fit": 340.2657,
                "se.fit": 0.0179,
                "lower_ci": 340.2119,
                "upper_ci": 340.3194
            },
            {
                "year": 2023,
                "fit": 341.9999,
                "se.fit": 0.0248,
                "lower_ci": 341.9254,
                "upper_ci": 342.0743
            }
        ]
        return Response(data=response)

        # species_name = request.GET.get("species")
        # start_year = request.GET.get("start_year")
        # end_year = request.GET.get("end_year")
        # property_list = request.GET.get('property')
        # property_ids = property_list.split(',') if property_list else []
        #
        # # Create a base query
        # query = Q()
        #
        # if species_name:
        #     query &= Q(
        #         owned_species__taxon__scientific_name=species_name
        #     )
        #
        # if property_list:
        #     property_ids = property_list.split(',')
        #     query &= Q(
        #         owned_species__property__id__in=property_ids
        #     )
        #
        # if start_year:
        #     query &= Q(year__gte=start_year)
        #
        # if end_year:
        #     query &= Q(year__lte=end_year)
        #
        # species = get_object_or_404(
        #     Taxon, scientific_name=species_name
        # )
        #
        # cached_json_data = get_statistical_model_output_cache(
        #         species, SPECIES_PER_PROPERTY)
        #
        # if cached_json_data:
        #     return Response(status=200, data=cached_json_data)
        #
        # statistical_model_output = StatisticalModelOutput.objects.filter(
        #     model__taxon=species,
        #     type=SPECIES_PER_PROPERTY
        # ).first()
        #
        # csv_headers = [
        #     'property', 'province', 'species', 'year', 'count_total',
        #     'survey_method', 'open_closed', 'property_type',
        #     'property_size', 'area_available_to_species'
        # ]
        #
        # rows = AnnualPopulation.objects.select_related(
        #     'owned_species', 'survey_method',
        #     'owned_species__taxon',
        #     'owned_species__property',
        #     'owned_species__property__province',
        #     'owned_species__property__property_type'
        # ).filter(
        #     query
        # ).order_by('year')
        #
        # rows_serialized = AnnualPopulationSerializer(
        #     rows,
        #     many=True
        # )
        #
        # rows = rows_serialized.data
        #
        # csv_data = []
        #
        # for row in rows:
        #     owned_species = row.get('owned_species')
        #     survey_method = row.get('survey_method')
        #     survey_method_name = ''
        #     if survey_method:
        #         survey_method_name = survey_method
        #     if owned_species is not None:
        #         data_row = [
        #             row.get('owned_species').property.name,
        #             row.get('owned_species__property__province').name,
        #             row.get('owned_species__taxon').scientific_name,
        #             row.get('year'),
        #             row.get('total'),
        #             survey_method_name,
        #             'Open' if owned_species.property.open else 'Closed',
        #             row.get('owned_species__property__property_type').name,
        #             row.get('owned_species').property.property_size_ha,
        #             row.get('area_available_to_species')
        #         ]
        #         csv_data.append(data_row)
        #
        #
        #
        # data_filepath = write_plumber_data(csv_headers, csv_data)
        #
        # statistical_model = (
        #     statistical_model_output.model if
        #     statistical_model_output else None
        # )
        #
        # is_success, json_data = execute_statistical_model(
        #     data_filepath, species, model=statistical_model)
        # # remove data_filepath
        # remove_plumber_data(data_filepath)
        # if is_success:
        #     species_population_trend_data = json_data.get(
        #         SPECIES_PER_PROPERTY, [])
        #     save_statistical_model_output_cache(
        #         species, SPECIES_PER_PROPERTY,
        #         species_population_trend_data
        #     )
        #     return Response(status=200, data=species_population_trend_data)
        # return Response(status=200, data=response)
