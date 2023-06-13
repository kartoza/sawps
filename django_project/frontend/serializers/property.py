"""Serializer for property classes."""
from frontend.serializers.common import NameObjectBaseSerializer
from property.models import (
    PropertyType,
    Province
)


class PropertyTypeSerializer(NameObjectBaseSerializer):
    """Property Type Serializer."""

    class Meta:
        model = PropertyType
        fields = NameObjectBaseSerializer.Meta.fields


class ProvinceSerializer(NameObjectBaseSerializer):
    """Province Serializer."""

    class Meta:
        model = Province
        fields = NameObjectBaseSerializer.Meta.fields
