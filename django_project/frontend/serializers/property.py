"""Serializer for property classes."""
from rest_framework import serializers
from frontend.serializers.common import NameObjectBaseSerializer
from property.models import (
    PropertyType,
    Province,
    Property
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


class PropertySerializer(serializers.ModelSerializer):
    """Property Serializer."""
    owner = serializers.SerializerMethodField()
    property_type = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()
    organisation = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    def get_owner(self, obj: Property):
        name = (
            f'{obj.created_by.first_name} {obj.created_by.last_name}'.strip()
        )
        return name if name else obj.created_by.username

    def get_property_type(self, obj: Property):
        return obj.property_type.name

    def get_province(self, obj: Property):
        return obj.province.name

    def get_organisation(self, obj: Property):
        return obj.organisation.name

    def get_size(self, obj: Property):
        return obj.property_size_ha

    class Meta:
        model = Property
        fields = [
            'id', 'name', 'owner',
            'property_type', 'property_type_id',
            'province', 'province_id',
            'size', 'organisation', 'organisation_id'
        ]
