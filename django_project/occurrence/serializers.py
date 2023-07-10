from rest_framework import serializers
from occurrence.models import SurveyMethod, SamplingSizeUnit


class SurveyMethodSerializer(serializers.ModelSerializer):
    """SurveyMethod serializer"""

    class Meta():
        model = SurveyMethod
        fields = ['id', 'name']


class SamplingSizeUnitSerializer(serializers.ModelSerializer):
    """SamplingSizeUnit serializer"""
    name = serializers.CharField(source='unit')

    class Meta():
        model = SamplingSizeUnit
        fields = ['id', 'name']
