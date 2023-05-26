""" add serializers to the spatial layer's model """

from rest_framework_gis import serializers
from . import models

# explore different types of serializers


class FeatureSerializer(serializers.GeoFeatureModelSerializer):
    """serializer for features"""

    class Meta:
        model = models.Feature
        geo_field = 'geom'
        auto_bbox = True
        fields = '__all__'


class VectorLayerSerializer(serializers.ModelSerializer):
    """
    serializer for vector layer's model
    """

    # didn't use source="features" because it's the same as attr name
    features = FeatureSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = models.VectorLayer
        fields = [
            'id',
            'name',
            'type',
            'extent',
            'srid',
            'description',
            'features',
        ]


class WMSLayerSerializer(serializers.ModelSerializer):
    """
    serializer for wms layer's model
    """

    class Meta:
        model = models.WMS
        fields = '__all__'


class RasterLayerSerializer(serializers.ModelSerializer):
    """
    serializer for Raster layer's model
    """

    class Meta:
        model = models.RasterLayer
        fields = '__all__'
