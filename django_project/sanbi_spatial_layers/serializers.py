""" add serializers to the spatial layer's model """

from rest_framework_gis import serializers
from . import models

# explore different types of serializers


class WMSLayerSerializer(serializers.ModelSerializer):
    """
    serializer for wms layer's model
    """

    class Meta:
        model = models.WMS
        fields = '__all__'
