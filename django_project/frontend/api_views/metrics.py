# -*- coding: utf-8 -*-

"""API Views related to metrics.
"""
from frontend.filters.metrics import (
    BaseMetricsFilter,
    SpeciesPopulationCountFilter,
)
from frontend.serializers.metrics import (
    ActivityMatrixSerializer,
    SpeciesPopulationCountSerializer,
    TotalCountPerActivitySerializer,
)
from frontend.static_mapping import ACTIVITY_COLORS_DICT
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from species.models import Taxon


class SpeciesPopulationCountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SpeciesPopulationCountSerializer

    def get_queryset(self, property_id):
        organisation_id = self.request.session.get('current_organisation_id')
        queryset = Taxon.objects.filter(
            ownedspecies__property__organisation_id=organisation_id,
            taxon_rank__name='Species', ownedspecies__property_id=property_id
        ).distinct()
        filtered_queryset = SpeciesPopulationCountFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset

    def get(self, request, property_id, *args, **kwargs):
        queryset = self.get_queryset(property_id=property_id)
        serializer = self.serializer_class(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data)


class ActivityPercentageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActivityMatrixSerializer

    def get_queryset(self):
        organisation_id = self.request.session.get('current_organisation_id')
        queryset = Taxon.objects.filter(
            ownedspecies__property__organisation_id=organisation_id,
            taxon_rank__name='Species'
        ).distinct()
        filtered_queryset = BaseMetricsFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset

    def get(self, request, *args, **kwargs):
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
    permission_classes = [IsAuthenticated]
    serializer_class = ActivityMatrixSerializer

    def get_queryset(self):
        organisation_id = self.request.session.get('current_organisation_id')
        queryset = Taxon.objects.filter(
            ownedspecies__property__organisation_id=organisation_id,
            taxon_rank__name='Species'
        ).distinct()
        filtered_queryset = BaseMetricsFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = TotalCountPerActivitySerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)
