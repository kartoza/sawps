"""API Views related to metrics.
"""
import datetime
from typing import List

import jenkspy
from django.db.models import Count
from django.db.models import FloatField
from django.db.models.functions import Cast
from django.db.models.query import QuerySet, F
from django.http import HttpRequest
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from frontend.filters.metrics import (
    ActivityBaseMetricsFilter,
    BaseMetricsFilter,
    PropertyFilter,
)
from frontend.serializers.metrics import (
    AreaAvailablePerSpeciesSerializer,
    ActivityMatrixSerializer,
    SpeciesPopuationCountPerYearSerializer,
    SpeciesPopulationDensityPerPropertySerializer,
    TotalCountPerActivitySerializer,
    PopulationPerAgeGroupSerialiser,
    TotalAreaVSAvailableAreaSerializer,
    TotalCountPerPopulationEstimateSerializer
)
from frontend.utils.data_table import (
    get_queryset, get_report_filter, SPECIES_REPORT
)
from frontend.utils.data_table import get_taxon_queryset, common_filters
from frontend.utils.metrics import (
    calculate_population_categories,
    calculate_total_area_per_property_type,
    calculate_base_population_of_species,
    calculate_species_count_per_province
)
from frontend.utils.organisation import (
    get_current_organisation_id
)
from frontend.utils.user_roles import get_user_roles
from population_data.models import AnnualPopulation
from property.models import Property
from species.models import Taxon


class SpeciesPopuationCountPerYearAPIView(APIView):
    """
    An API view to retrieve species population count per year.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = SpeciesPopuationCountPerYearSerializer

    def get_queryset(self) -> List[Taxon]:
        """
        Returns a filtered queryset of Taxon objects representing
        species within the specified organization.
        """
        organisation_id = get_current_organisation_id(self.request.user)
        queryset = Taxon.objects.filter(
            annualpopulation__property__organisation_id=organisation_id,
            taxon_rank__name='Species'
        ).distinct()
        filtered_queryset = BaseMetricsFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset

    def get(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        Handles HTTP GET requests and returns a serialized JSON response.
        Params: The HTTP request object containing the user's request data.
        """
        queryset = self.get_queryset()
        serializer = SpeciesPopuationCountPerYearSerializer(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data)


class ActivityPercentageAPIView(APIView):
    """
    API view to retrieve activity percentage data for species.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ActivityMatrixSerializer

    def get_queryset(self) -> List[Taxon]:
        """
        Returns a filtered queryset of Taxon objects representing
        species within the specified organization.
        """
        organisation_id = get_current_organisation_id(self.request.user)
        queryset = Taxon.objects.filter(
            annualpopulation__property__organisation_id=organisation_id,
            taxon_rank__name='Species'
        ).distinct()
        filtered_queryset = ActivityBaseMetricsFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle the GET request to retrieve activity percentage data.
        Params: request (Request): The HTTP request object.
        """
        queryset = self.get_queryset()
        serializer = ActivityMatrixSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(calculate_base_population_of_species(serializer.data))


class TotalCountPerPopulationEstimateAPIView(APIView):
    """
    API view to retrieve total counts per population
    estimate category for species.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        serializer = TotalCountPerPopulationEstimateSerializer(
            context={"request": request}
        )
        result = serializer.get_total_counts_per_population_estimate()
        return Response(result)


class TotalCountPerActivityAPIView(APIView):
    """
    API view to retrieve total counts per activity for species.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ActivityMatrixSerializer

    def get_queryset(self) -> List[Taxon]:
        """
        Returns a filtered queryset of Taxon objects representing
        species within the specified organization.
        """
        organisation_id = get_current_organisation_id(self.request.user)
        queryset = Taxon.objects.filter(
            annualpopulation__property__organisation_id=organisation_id,
            taxon_rank__name='Species'
        ).distinct()
        filtered_queryset = ActivityBaseMetricsFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle the GET request to retrieve total counts per activity data.
        Params:request (Request): The HTTP request object.
        """
        queryset = self.get_queryset()
        serializer = TotalCountPerActivitySerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class SpeciesPopulationCountPerProvinceAPIView(APIView):
    """
    API view to retrieve species pcount per province.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Property]:
        """
        Returns a filtered queryset of property objects
        within the specified organization.
        """

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET request to retrieve species count per province.
        """
        user_roles = get_user_roles(request.user)
        queryset = get_taxon_queryset(request)
        filters = common_filters(request, user_roles)

        return Response(
            calculate_species_count_per_province(
                queryset.first(),
                filters
            )
        )


class SpeciesPopulationDensityPerPropertyAPIView(APIView):
    """
    API view to retrieve species population density per property.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SpeciesPopulationDensityPerPropertySerializer

    def get_queryset(self) -> QuerySet[Property]:
        """
        Returns a filtered queryset of property objects
        within the specified organization.
        """
        organisation_id = get_current_organisation_id(self.request.user)
        queryset = Property.objects.filter(organisation_id=organisation_id)
        filtered_queryset = PropertyFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset.distinct('name')

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle the GET request to retrieve species
        population density per property.
        Params:request (Request): The HTTP request object.
        """
        queryset = self.get_queryset()

        # Extract the species_name query parameter from the URL
        species_name = self.request.query_params.get("species", None)

        serializer = SpeciesPopulationDensityPerPropertySerializer(
            queryset,
            many=True,
            context={
                "request": request,
                "species_name": species_name
            }
        )
        return Response(serializer.data)


class PropertiesPerPopulationCategoryAPIView(APIView):
    """
    API endpoint to retrieve population categories
    for properties within an organization.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Property]:
        """
        Get the filtered queryset of properties owned by the organization.
        """
        organisation_id = get_current_organisation_id(self.request.user)
        queryset = Property.objects.filter(organisation_id=organisation_id)
        filtered_queryset = PropertyFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET request to retrieve population categories for properties.
        """
        species_name = request.GET.get("species")
        start_year = request.GET.get("start_year", 0)
        end_year = request.GET.get("end_year", datetime.datetime.now().year)
        year_range = (int(start_year), int(end_year))
        queryset = self.get_queryset()
        return Response(
            calculate_population_categories(queryset, species_name, year_range)
        )


class TotalAreaAvailableToSpeciesAPIView(APIView):
    """
    An API view to retrieve total area available to species.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        Retrieve the calculated total area available to species and
        return it as a Response.
        """
        user_roles = get_user_roles(request.user)
        queryset = get_queryset(user_roles, request)
        filters = get_report_filter(request, SPECIES_REPORT)
        if 'annualpopulationperactivity__activity_type_id__in' in filters:
            del filters['annualpopulationperactivity__activity_type_id__in']
        species_population_data = AnnualPopulation.objects.filter(
            property__in=queryset,
            **filters
        )
        return Response(
            AreaAvailablePerSpeciesSerializer(
                species_population_data, many=True
            ).data
        )


class TotalAreaPerPropertyTypeAPIView(APIView):
    """
    API endpoint to retrieve total area per property type
    for properties within an organization.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Property]:
        """
        Get the filtered queryset of properties owned by the organization.
        """
        organisation_id = get_current_organisation_id(self.request.user)
        queryset = Property.objects.filter(organisation_id=organisation_id)
        filtered_queryset = PropertyFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET request to retrieve total area per property type.
        """
        species_name = request.GET.get("species")
        queryset = self.get_queryset()
        return Response(
            calculate_total_area_per_property_type(
                queryset, species_name)
        )


class PopulationPerAgeGroupAPIView(APIView):
    """
    API endpoint to retrieve population of age group.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Taxon]:
        """
        Get the filtered queryset taxon owned by the organization.
        """
        organisation_id = get_current_organisation_id(self.request.user)
        queryset = Taxon.objects.filter(
            annualpopulation__property__organisation_id=organisation_id,
            taxon_rank__name='Species'
        ).distinct()
        filtered_queryset = BaseMetricsFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle the GET request to retrieve population of age groups.
        Params:request (Request): The HTTP request object.
        """
        queryset = self.get_queryset()
        serializer = PopulationPerAgeGroupSerialiser(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class TotalAreaVSAvailableAreaAPIView(APIView):
    """
    API endpoint to retrieve total area and area available.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> List[Taxon]:
        """
        Returns a filtered queryset of Taxon objects representing
        species within the specified organization.
        """
        organisation_id = get_current_organisation_id(self.request.user)
        queryset = Taxon.objects.filter(
            annualpopulation__property__organisation_id=organisation_id,
            taxon_rank__name='Species'
        ).distinct()
        filtered_queryset = BaseMetricsFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET request to retrieve total area and available area.
        """
        queryset = self.get_queryset()
        serializer = TotalAreaVSAvailableAreaSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class BasePropertyCountAPIView(APIView):
    """
    Base class for property count APIView
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> List[AnnualPopulation]:
        """
        Returns a filtered queryset of Taxon objects
        """
        property_list = self.request.GET.get("property")
        year_filter = self.request.GET.get('year', None)
        taxon_filter = self.request.GET.get('species', None)

        filters = {}

        if year_filter:
            filters['year'] = year_filter
        if taxon_filter:
            filters['taxon__scientific_name'] = taxon_filter

        if property_list:
            property_ids = property_list.split(",")
            filters['property_id__in'] = property_ids

        queryset = AnnualPopulation.objects.filter(
            **filters
        ).distinct()
        return queryset

    def get_upper_lower_bound(self, categories, idx, category, query_field):
        lower_bound = category
        upper_bound = categories[idx + 1]
        delta = 1
        if query_field == 'population_density':
            delta = 0.00001

        if lower_bound == upper_bound:
            lower_bound -= 2 * delta
            upper_bound -= delta
        else:
            upper_bound -= delta

        if idx == len(categories) - 2:
            upper_bound = categories[idx + 1]

        if idx == len(categories) - 3:
            upper_bound = categories[idx + 1]

        if query_field == 'population_density':
            lower_bound = round(lower_bound, 2)
            upper_bound = round(upper_bound, 2)
        else:
            lower_bound = round(lower_bound)
            upper_bound = round(upper_bound)

        return lower_bound, upper_bound

    def get_results(self, data: set, queryset: QuerySet,
                    property_type_name_field: str,
                    common_name: str, query_field: str):
        categories = jenkspy.jenks_breaks(
            data,
            n_classes=data.count() if data.count() < 6 else 6
        )
        if query_field == 'population_density':
            categories = sorted([round(cat, 2) for cat in categories])
        else:
            categories = sorted([round(cat) for cat in categories])

        results = []
        for idx, category in enumerate(categories):
            if idx != len(categories) - 1:
                lower_bound, upper_bound = self.get_upper_lower_bound(
                    categories,
                    idx,
                    category,
                    query_field
                )

                if lower_bound < 0:
                    continue

                category_annotation = f'{lower_bound} - {upper_bound}'
                filters = {f'{query_field}__range': (lower_bound, upper_bound)}
                if idx == len(categories) - 2 and len(categories) > 2:
                    category_annotation = f'>{lower_bound}'
                    filters = {f'{query_field}__gt': lower_bound}

                counts = queryset.filter(
                    **filters
                ).values(property_type_name_field).annotate(
                    count=Count(property_type_name_field)
                )

                result = {
                    'category': category_annotation,
                    'common_name_varbatim': common_name
                }
                for count in counts:
                    result[
                        count[
                            property_type_name_field
                        ].lower().replace(' ', '_')
                    ] = count['count']
                if counts.exists():
                    results.append(result)
        return results


class PropertyCountPerPopulationSizeCategoryAPIView(BasePropertyCountAPIView):
    """
    API endpoint to property count per population size category
    """

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET request to retrieve property count
        per population size category.
        """
        results = []
        queryset = self.get_queryset()
        data = queryset.values_list('total', flat=True).distinct()
        if not data.exists():
            return Response(results)

        common_name = queryset.first().taxon.common_name_varbatim
        results = self.get_results(
            data,
            queryset,
            'property__property_type__name',
            common_name,
            'total'
        )

        return Response(results)


class PropertyCountPerAreaCategoryAPIView(BasePropertyCountAPIView):
    """
    API endpoint to property count per area category
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET request to retrieve property count per area category.
        """
        results = []
        annual_populations = self.get_queryset()
        if not annual_populations.exists():
            return Response(results)
        queryset = Property.objects.filter(
            id__in=annual_populations.values_list(
                'property_id', flat=True
            )
        )

        data = queryset.values_list('property_size_ha', flat=True).distinct()

        common_name = annual_populations.first().taxon.common_name_varbatim
        results = self.get_results(
            data,
            queryset,
            'property_type__name',
            common_name,
            'property_size_ha'
        )

        return Response(results)


class PropertyPerAreaAvailableCategoryAPIView(BasePropertyCountAPIView):
    """
    API endpoint to property count per area available to species category
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET request to retrieve property count per
        area available to species category.
        """
        results = []
        queryset = self.get_queryset()
        data = queryset.values_list(
            'area_available_to_species',
            flat=True
        ).distinct()
        if not data.exists():
            return Response(results)

        common_name = queryset.first().taxon.common_name_varbatim
        results = self.get_results(
            data,
            queryset,
            'property__property_type__name',
            common_name,
            'area_available_to_species'
        )

        return Response(results)


class PropertyPerPopDensityCategoryAPIView(BasePropertyCountAPIView):
    """
    API endpoint to property count per population density category
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET request to retrieve property count
        per population density category.
        """
        results = []
        queryset = self.get_queryset()
        queryset = queryset.exclude(area_available_to_species=0).annotate(
            population_density=Cast(
                Cast(F('total'), FloatField()) /
                Cast(F('area_available_to_species'), FloatField()),
                FloatField()
            )
        )
        data = queryset.values_list('population_density', flat=True).distinct()
        if not data.exists():
            return Response(results)

        common_name = queryset.first().taxon.common_name_varbatim
        results = self.get_results(
            data,
            queryset,
            'property__property_type__name',
            common_name,
            'population_density'
        )

        return Response(results)
