from rest_framework import serializers

from .models import (
    SurveyMethod,
    SamplingSizeUnit
)


class SurveyMethodSerializer(serializers.ModelSerializer):
    """Survey Method Serializer"""

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(SurveyMethodSerializer, self).__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    class Meta:
        model = SurveyMethod
        fields = '__all__'


class SamplingSizeUnitSerializer(serializers.ModelSerializer):
    """SamplingSizeUnit Serializer"""

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(SamplingSizeUnitSerializer, self).__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    class Meta:
        model = SamplingSizeUnit
        fields = '__all__'


class SamplingSizeUnitMetadataSerializer(serializers.ModelSerializer):
    """SamplingSizeUnit Serializer with id and name."""
    name = serializers.CharField(source='unit')

    class Meta:
        model = SamplingSizeUnit
        fields = ['id', 'name']
