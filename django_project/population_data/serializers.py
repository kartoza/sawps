from rest_framework import serializers
from population_data.models import (
    OpenCloseSystem,
    CountMethod
)


class CountMethodSerializer(serializers.ModelSerializer):
    """CountMethod serializer"""

    class Meta():
        model = CountMethod
        fields = ['id', 'name']


class OpenCloseSystemSerializer(serializers.ModelSerializer):
    """OpenCloseSystem serializer"""

    class Meta():
        model = OpenCloseSystem
        fields = ['id', 'name']
