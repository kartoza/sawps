"""API Views related to metrics.
"""
from typing import List
from django.db.models.query import QuerySet
from django.http import HttpRequest
from frontend.filters.metrics import (
    ActivityBaseMetricsFilter,
    BaseMetricsFilter,
    PropertyFilter,
)
from frontend.serializers.metrics import (
    ActivityMatrixSerializer,
    SpeciesPopuationCountPerYearSerializer,
    SpeciesPopulationTotalAndDensitySerializer,
    TotalCountPerActivitySerializer,
)
from frontend.static_mapping import ACTIVITY_COLORS_DICT
from frontend.utils.metrics import calculate_population_categories
from property.models import Property
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
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
        organisation_id = self.request.session.get('current_organisation_id')
        queryset = Taxon.objects.filter(
            ownedspecies__property__organisation_id=organisation_id,
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
        organisation_id = self.request.session.get('current_organisation_id')
        queryset = Taxon.objects.filter(
            ownedspecies__property__organisation_id=organisation_id,
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
        serializer_data = {
            "data": serializer.data,
            "activity_colours": ACTIVITY_COLORS_DICT
        }
        return Response(serializer_data)


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
        organisation_id = self.request.session.get('current_organisation_id')
        queryset = Taxon.objects.filter(
            ownedspecies__property__organisation_id=organisation_id,
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


class SpeciesPopulationTotalAndDensityAPIView(APIView):
    """
    API view to retrieve species population total and density data for specie.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ActivityMatrixSerializer

    def get_queryset(self) -> List[Taxon]:
        """
        Returns a filtered queryset of Taxon objects representing
        species within the specified organization.
        """
        organisation_id = self.request.session.get('current_organisation_id')
        queryset = Taxon.objects.filter(
            ownedspecies__property__organisation_id=organisation_id,
            taxon_rank__name='Species'
        ).distinct()
        filtered_queryset = BaseMetricsFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle the GET request to retrieve species
        population total and density data.
        Params:request (Request): The HTTP request object.
        """
        queryset = self.get_queryset()
        serializer = SpeciesPopulationTotalAndDensitySerializer(
            queryset, many=True, context={"request": request}
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
        organisation_id = self.request.session.get('current_organisation_id')
        queryset = Property.objects.filter(organisation_id=organisation_id)
        filtered_queryset = PropertyFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET request to retrieve population categories for properties.
        """
        queryset = self.get_queryset()
        return Response(calculate_population_categories(queryset))
