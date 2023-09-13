"""Serializers for population data package.
"""
from rest_framework import serializers

from .models import (
    CountMethod,
    OpenCloseSystem,
    PopulationEstimateCategory,
    PopulationStatus,
    SamplingEffortCoverage,
)


class CountMethodSerializer(serializers.ModelSerializer):
    """Count Method Serializer"""

    class Meta:
        model = CountMethod
        fields = '__all__'


class OpenCloseSystemSerializer(serializers.ModelSerializer):
    """OpenClose System Serializer"""

    class Meta:
        model = OpenCloseSystem
        fields = '__all__'


class SamplingEffortCoverageSerializer(serializers.ModelSerializer):
    """SamplingEffortCoverage Serializer"""

    class Meta:
        model = SamplingEffortCoverage
        fields = '__all__'


class PopulationStatusSerializer(serializers.ModelSerializer):
    """PopulationStatus Serializer"""

    class Meta:
        model = PopulationStatus
        fields = '__all__'


class PopulationEstimateCategorySerializer(serializers.ModelSerializer):
    """PopulationEstimateCategory Serializer"""

    class Meta:
        model = PopulationEstimateCategory
        fields = '__all__'
