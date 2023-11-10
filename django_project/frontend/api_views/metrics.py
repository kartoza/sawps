"""API Views related to metrics.
"""
import datetime
import jenkspy
from typing import List

from django.utils import timezone
from django.db.models.query import QuerySet
from django.http import HttpRequest
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Value

from frontend.filters.metrics import (
    ActivityBaseMetricsFilter,
    BaseMetricsFilter,
    PropertyFilter,
)
from frontend.serializers.metrics import (
    ActivityMatrixSerializer,
    SpeciesPopuationCountPerYearSerializer,
    SpeciesPopulationDensityPerPropertySerializer,
    TotalCountPerActivitySerializer,
    PopulationPerAgeGroupSerialiser,
    TotalAreaVSAvailableAreaSerializer,
    TotalCountPerPopulationEstimateSerializer,
    PropertyCountPerPopulationSizeCategorySerialiser
)
from frontend.serializers.metrics import AreaAvailablePerSpeciesSerializer
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
from property.models import Property, PropertyType
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

    def get_queryset(self) -> QuerySet[Property]:
        """
        Get the filtered queryset of properties for the current organization.
            """
        organisation_id = get_current_organisation_id(self.request.user)
        queryset = Property.objects.filter(organisation_id=organisation_id)
        filtered_queryset = PropertyFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset.distinct('name')

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

        filters = {
            'year': self.request.GET.get("year", timezone.now().year),
            'taxon__scientific_name': self.request.GET.get("species", ''),
        }

        if property_list:
            property_ids = property_list.split(",")
            filters['property_id__in'] = property_ids

        queryset = AnnualPopulation.objects.filter(
            **filters
        ).distinct()
        return queryset

    def get_upper_lower_bound(self, categories, idx, category):
        lower_bound = category
        upper_bound = categories[idx + 1]
        if lower_bound == upper_bound:
            lower_bound -= 2
            upper_bound -= 1
        else:
            upper_bound -= 1

        if idx == len(categories) - 2:
            upper_bound = categories[idx + 1]
        return lower_bound, upper_bound


class PropertyCountPerPopulationSizeCategoryAPIView(BasePropertyCountAPIView):
    """
    API endpoint to property count per population size category
    """

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET request to retrieve property count per population size category.
        """
        results = []
        queryset = self.get_queryset()
        data = queryset.values_list('total', flat=True).distinct()
        if not data.exists():
            return Response(results)

        common_name = queryset.first().taxon.common_name_varbatim

        categories = jenkspy.jenks_breaks(
            data,
            n_classes=data.count() if data.count() < 6 else 6
        )
        property_types = PropertyType.objects.values_list('name', flat=True)
        base_dict = {property_type: 0 for property_type in property_types}
        base_dict['common_name_varbatim'] = common_name

        for idx, category in enumerate(categories):
            if idx != len(categories) - 1:
                lower_bound, upper_bound = self.get_upper_lower_bound(
                    categories,
                    idx,
                    category
                )

                counts = queryset.filter(
                    total__range=(lower_bound, upper_bound)
                ).values('property__property_type__name').annotate(
                    count=Count('property__property_type__name'),
                    category=Value(f'{lower_bound} - {upper_bound}')
                )
                result = {
                    'category': f'{lower_bound} - {upper_bound}'
                }
                result.update(base_dict)
                for count in counts:
                    result[
                        count['property__property_type__name'].lower().replace(' ', ' ')
                    ] = count['count']
                results.append(result)

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
        queryset = Property.objects.filter(id__in=annual_populations.values_list('property_id', flat=True))

        data = queryset.values_list('property_size_ha', flat=True).distinct()

        common_name = annual_populations.first().taxon.common_name_varbatim

        categories = jenkspy.jenks_breaks(
            data,
            n_classes=data.count() if data.count() < 6 else 6
        )
        property_types = PropertyType.objects.values_list('name', flat=True)
        base_dict = {property_type: 0 for property_type in property_types}
        base_dict['common_name_varbatim'] = common_name

        for idx, category in enumerate(categories):
            if idx != len(categories) - 1:
                lower_bound, upper_bound = self.get_upper_lower_bound(
                    categories,
                    idx,
                    category
                )

                counts = queryset.filter(
                    property_size_ha__range=(lower_bound, upper_bound)
                ).values('property_type__name').annotate(
                    count=Count('property_type__name'),
                    category=Value(f'{lower_bound} - {upper_bound}')
                )
                result = {
                    'category': f'{lower_bound} - {upper_bound}'
                }
                result.update(base_dict)
                for count in counts:
                    result[
                        count['property_type__name'].lower().replace(' ', ' ')
                    ] = count['count']
                results.append(result)

        return Response(results)


# class PropertyCountPerAreaCategoryAPIView(BasePropertyCountAPIView):
#     """
#     API endpoint to property count per area category
#     """
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, *args, **kwargs) -> Response:
#         """
#         Handle GET request to retrieve property count per area category.
#         """
#         results = []
#         annual_populations = self.get_queryset()
#         if not annual_populations.exists():
#             return Response(results)
#         queryset = Property.objects.filter(id__in=annual_populations.values_list('property_id', flat=True))
#
#         data = queryset.values_list('property_size_ha', flat=True).distinct()
#
#         common_name = annual_populations.first().taxon.common_name_varbatim
#
#         categories = jenkspy.jenks_breaks(
#             data,
#             n_classes=data.count() if data.count() < 6 else 6
#         )
#         property_types = PropertyType.objects.values_list('name', flat=True)
#         base_dict = {property_type: 0 for property_type in property_types}
#         base_dict['common_name_varbatim'] = common_name
#
#         for idx, category in enumerate(categories):
#             if idx != len(categories) - 1:
#                 lower_bound, upper_bound = self.get_upper_lower_bound(
#                     categories,
#                     idx,
#                     category
#                 )
#
#                 counts = queryset.filter(
#                     property_size_ha__range=(lower_bound, upper_bound)
#                 ).values('property_type__name').annotate(
#                     count=Count('property_type__name'),
#                     category=Value(f'{lower_bound} - {upper_bound}')
#                 )
#                 result = {
#                     'category': f'{lower_bound} - {upper_bound}'
#                 }
#                 result.update(base_dict)
#                 for count in counts:
#                     result[
#                         count['property_type__name'].lower().replace(' ', ' ')
#                     ] = count['count']
#                 results.append(result)
#
#         return Response(results)
