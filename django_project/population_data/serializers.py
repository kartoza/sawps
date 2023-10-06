"""Serializers for population data package.
"""
from rest_framework import serializers

from .models import (
    OpenCloseSystem,
    PopulationEstimateCategory,
    PopulationStatus,
    SamplingEffortCoverage,
    Certainty
)


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


class CertaintySerializer(serializers.ModelSerializer):
    """Certainty Serializer"""
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_id(self, obj: Certainty):
        return int(obj.name)

    def get_name(self, obj: Certainty):
        return obj.description

    class Meta:
        model = Certainty
        fields = ['id', 'name']
