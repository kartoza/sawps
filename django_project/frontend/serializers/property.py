"""Serializer for property classes."""
from rest_framework import serializers
from frontend.serializers.common import NameObjectBaseSerializer
from property.models import (
    PropertyType,
    Province,
    Property,
    Parcel
)


class PropertyTypeSerializer(NameObjectBaseSerializer):
    """Property Type Serializer."""

    class Meta:
        model = PropertyType
        fields = NameObjectBaseSerializer.Meta.fields


class PropertyTypeColourSerializer(serializers.ModelSerializer):
    """Property Type Serializer with Colour."""

    class Meta:
        model = PropertyType
        fields = [
            'id',
            'name',
            'colour'
        ]


class ProvinceSerializer(NameObjectBaseSerializer):
    """Province Serializer."""

    class Meta:
        model = Province
        fields = NameObjectBaseSerializer.Meta.fields


class PropertySerializer(serializers.ModelSerializer):
    """Property Serializer."""

    owner = serializers.SerializerMethodField()
    owner_email = serializers.SerializerMethodField()
    property_type = serializers.SerializerMethodField()
    open = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()
    organisation = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    def get_owner(self, obj: Property):
        name = (
            f'{obj.created_by.first_name} {obj.created_by.last_name}'.strip()
        )
        return name if name else obj.created_by.username

    def get_owner_email(self, obj: Property):
        return obj.created_by.email

    def get_property_type(self, obj: Property):
        return obj.property_type.name

    def get_open(self, obj: Property):
        return obj.open.name if obj.open else ''

    def get_province(self, obj: Property):
        return obj.province.name

    def get_organisation(self, obj: Property):
        return obj.organisation.name

    def get_size(self, obj: Property):
        return obj.property_size_ha


    class Meta:
        model = Property
        fields = [
            'id', 'name', 'owner', 'owner_email',
            'property_type', 'property_type_id',
            'province', 'province_id',
            'open', 'open_id',
            'size', 'organisation', 'organisation_id',
            'short_code', 'boundary_source'
        ]


class ParcelSerializer(serializers.ModelSerializer):
    """Parcel Serializer."""
    layer = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    cname = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    def get_id(self, obj: Parcel):
        return obj.source_id

    def get_cname(self, obj: Parcel):
        return obj.sg_number

    def get_layer(self, obj: Parcel):
        return obj.source

    def get_type(self, obj: Parcel):
        return obj.parcel_type.name.lower()

    class Meta:
        model = Parcel
        fields = [
            'id', 'layer', 'type', 'cname'
        ]


class PropertyDetailSerializer(PropertySerializer):
    """Property with more details."""
    parcels = serializers.SerializerMethodField()
    bbox = serializers.SerializerMethodField()
    centroid = serializers.SerializerMethodField()

    def get_parcels(self, obj: Property):
        parcels = obj.parcel_set.all()
        return ParcelSerializer(parcels, many=True).data

    def get_bbox(self, obj: Property):
        if obj.geometry is None:
            return []
        return list(obj.geometry.envelope.extent)

    def get_centroid(self, obj: Property):
        if obj.geometry is None:
            return []
        return list(obj.geometry.centroid)

    class Meta:
        model = Property
        fields = [
            'id', 'name', 'owner', 'owner_email',
            'property_type', 'property_type_id',
            'open', 'open_id',
            'province', 'province_id',
            'size', 'organisation', 'organisation_id',
            'parcels', 'bbox', 'centroid', 'short_code',
            'boundary_source'
        ]


class PropertySearchSerializer(PropertyDetailSerializer):
    """Return id, name, bbox of property."""
    id = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_id(self, obj: Property):
        return f'property-{obj.id}'

    def get_type(self, obj: Property):
        return 'property'

    def get_name(self, obj: Property):
        return f'{obj.name} ({obj.short_code})'

    class Meta:
        model = Property
        fields = [
            'id', 'type', 'name', 'bbox'
        ]
