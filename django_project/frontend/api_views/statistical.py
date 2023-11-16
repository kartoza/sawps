# -*- coding: utf-8 -*-

"""API Views related to statistical.
"""
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from frontend.models.base_task import DONE
from species.models import Taxon
from frontend.models import (
    SpeciesModelOutput,
    NATIONAL_TREND
)


class SpeciesNationalTrend(APIView):
    """Fetch national trend of species."""
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        species_id = kwargs.get('species_id')
        species = get_object_or_404(Taxon, id=species_id)
        # get latest species model output
        model_output = SpeciesModelOutput.objects.filter(
            taxon=species,
            is_latest=True,
            status=DONE
        ).first()
        if model_output:
            cache_key = model_output.get_cache_key(NATIONAL_TREND)
            cached_data = cache.get(cache_key)
            return Response(status=200, data=cached_data)
        return Response(status=200, data=[])


class SpeciesTrend(APIView):
    """Fetch trend of species based on specified criteria.

    This view allows users to retrieve national trend
    data for a specific species.

    Args:
        request: The HTTP request object containing query parameters.

    Returns:
        Response: JSON response containing trend data.

    """
    permission_classes = [AllowAny]

    def get(self, request):
        species_name = request.GET.get("species")
        species = get_object_or_404(
            Taxon, scientific_name=species_name
        )
        # get latest species model output
        model_output = SpeciesModelOutput.objects.filter(
            taxon=species,
            is_latest=True,
            status=DONE
        ).first()
        if model_output:
            cache_key = model_output.get_cache_key(NATIONAL_TREND)
            cached_data = cache.get(cache_key)
            return Response(status=200, data=cached_data)
        return Response(status=200, data=[])
