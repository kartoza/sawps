"""Serializer for BoundaryFile model."""
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from frontend.models.boundary_search import BoundaryFile, BoundarySearchRequest


class BoundaryFileSerializer(serializers.ModelSerializer):
    """Serializer for BoundaryFile."""

    class Meta:
        model = BoundaryFile
        fields = '__all__'


class BoundarySearchRequestGeoJsonSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = BoundarySearchRequest
        geo_field = 'geometry'
        fields = ['session']
