from rest_framework import serializers

from .models import (
    AnnualPopulation,
    AnnualPopulationPerActivity,
    CountMethod,
    OpenCloseSystem,
)
from occurrence.serializers import (
    SurveyMethodSerializer,
    SamplingSizeUnitSerializer,
)
from activity.serializers import ActivityTypeSerializer


class CountMethodSerializer(serializers.ModelSerializer):
    """Count Method Serializer"""

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(CountMethodSerializer, self).__init__(*args, **kwargs)
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
        super(OpenCloseSystemSerializer, self).__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    class Meta:
        model = OpenCloseSystem
        fields = '__all__'


class AnnualPopulationSerializer(serializers.ModelSerializer):
    """Population Count Serializer"""

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(AnnualPopulationSerializer, self).__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    month = serializers.StringRelatedField()
    count_method = serializers.SerializerMethodField()
    survey_method = serializers.SerializerMethodField()
    open_close_system = serializers.SerializerMethodField()
    sampling_size_unit = serializers.SerializerMethodField()


    class Meta:
        model = AnnualPopulation
        fields = '__all__'

    def get_count_method(self, obj):
        obj = obj.count_method
        serializer = CountMethodSerializer(
            obj,
            remove_fields=['id'],
        )
        return serializer.data

    def get_open_close_system(self, obj):
        obj = obj.open_close_system
        serializer = OpenCloseSystemSerializer(
            obj,
            remove_fields=['id'],
        )
        return serializer.data

    def get_survey_method(self, obj):
        obj = obj.survey_method
        serializer = SurveyMethodSerializer(
            obj,
            remove_fields=['id'],
        )
        return serializer.data

    def get_sampling_size_unit(self, obj):
        obj = obj.sampling_size_unit
        serializer = SamplingSizeUnitSerializer(
            obj,
            remove_fields=['id'],
        )
        return serializer.data


class AnnualPopulationPerActivitySerializer(serializers.ModelSerializer):
    """AnnualPopulation Per Activity Serializer"""
    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(
            AnnualPopulationPerActivitySerializer,
            self
        ).__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    month = serializers.StringRelatedField()
    count_method = serializers.SerializerMethodField()
    survey_method = serializers.SerializerMethodField()
    open_close_system = serializers.SerializerMethodField()
    sampling_size_unit = serializers.SerializerMethodField()
    activity_type = serializers.SerializerMethodField()

    class Meta:
        model = AnnualPopulationPerActivity
        fields = '__all__'

    def get_count_method(self, obj):
        obj = obj.count_method
        serializer = CountMethodSerializer(
            obj,
            remove_fields=['id'],
        )
        return serializer.data

    def get_open_close_system(self, obj):
        obj = obj.open_close_system
        serializer = OpenCloseSystemSerializer(
            obj,
            remove_fields=['id'],
        )
        return serializer.data

    def get_survey_method(self, obj):
        obj = obj.survey_method
        serializer = SurveyMethodSerializer(
            obj,
            remove_fields=['id'],
        )
        return serializer.data

    def get_sampling_size_unit(self, obj):
        obj = obj.sampling_size_unit
        serializer = SamplingSizeUnitSerializer(
            obj,
            remove_fields=['id'],
        )
        return serializer.data

    def get_activity_type(self, obj):
        obj = obj.activity_type
        serializer = ActivityTypeSerializer(
            obj,
            remove_fields=['id'],
        )
        return serializer.data
