"""Base serializer for common classes."""
from rest_framework import serializers


class NameObjectBaseSerializer(serializers.ModelSerializer):
    """Base Serializer for object with id and name."""

    class Meta:
        fields = ['id', 'name']
