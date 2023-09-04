# -*- coding: utf-8 -*-


"""Serializers for population data package.
"""
from rest_framework import serializers

from .models import (
    AnnualPopulation,
    AnnualPopulationPerActivity,
    CountMethod,
    OpenCloseSystem,
    SamplingEffortCoverage,
    PopulationStatus,
    PopulationEstimateCategory
)


class CountMethodSerializer(serializers.ModelSerializer):
    """Count Method Serializer"""

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super().__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    class Meta:
        model = CountMethod
        fields = '__all__'


class OpenCloseSystemSerializer(serializers.ModelSerializer):
    """OpenClose System Serializer"""

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super().__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    class Meta:
        model = OpenCloseSystem
        fields = '__all__'


class AnnualPopulationSerializer(serializers.ModelSerializer):
    """AnnualPopulation Serializer"""

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super().__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    month = serializers.StringRelatedField()
    count_method = serializers.SerializerMethodField()
    survey_method = serializers.SerializerMethodField()
    survey_method_sort_id = serializers.SerializerMethodField()
    open_close_system = serializers.SerializerMethodField()
    sampling_size_unit = serializers.SerializerMethodField()


    class Meta:
        model = AnnualPopulation
        fields = '__all__'

    def get_count_method(self, obj):
        return obj.count_method.name if obj.count_method else None

    def get_open_close_system(self, obj):
        return obj.open_close_system.name if obj.open_close_system else None

    def get_survey_method(self, obj):
        return obj.survey_method.name if obj.survey_method else None

    def get_survey_method_sort_id(self, obj):
        return obj.survey_method.sort_id if obj.survey_method else None

    def get_sampling_size_unit(self, obj):
        return obj.sampling_size_unit.unit if obj.sampling_size_unit else None


class AnnualPopulationPerActivitySerializer(serializers.ModelSerializer):
    """AnnualPopulationPerActivity Serializer"""

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super().__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    month = serializers.StringRelatedField()
    activity_type = serializers.SerializerMethodField()
    activity_type_recruitment = serializers.SerializerMethodField()

    class Meta:
        model = AnnualPopulationPerActivity
        fields = '__all__'

    def get_activity_type(self, obj):
        return obj.activity_type.name if obj.activity_type else None

    def get_activity_type_recruitment(self, obj):
        return obj.activity_type.recruitment if obj.activity_type else None


class SamplingEffortCoverageSerializer(serializers.ModelSerializer):
    """SamplingEffortCoverage Serializer"""

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super().__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    class Meta:
        model = SamplingEffortCoverage
        fields = '__all__'


class PopulationStatusSerializer(serializers.ModelSerializer):
    """PopulationStatus Serializer"""

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super().__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    class Meta:
        model = PopulationStatus
        fields = '__all__'


class PopulationEstimateCategorySerializer(serializers.ModelSerializer):
    """PopulationEstimateCategory Serializer"""

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super().__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    class Meta:
        model = PopulationEstimateCategory
        fields = '__all__'
