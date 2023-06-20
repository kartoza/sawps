"""Serializer for BoundaryFile model."""
from rest_framework import serializers
from frontend.models.boundary_search import BoundaryFile


class BoundaryFileSerializer(serializers.ModelSerializer):
    """Serializer for BoundaryFile."""

    class Meta:
        model = BoundaryFile
        fields = '__all__'
