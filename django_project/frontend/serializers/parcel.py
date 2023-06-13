"""Serializers for Parcel."""
from rest_framework import serializers
from frontend.models.parcels import (
    Erf,
    FarmPortion,
    Holding,
    ParentFarm
)


class ParcelBaseSerializer(serializers.ModelSerializer):
    """Parcel Base Serializer."""
    layer = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'cname', 'layer', 'type']


class ErfParcelSerializer(ParcelBaseSerializer):
    """Serializer for Erf."""

    def get_layer(self, obj):
        return 'erf'

    def get_type(self, obj):
        return 'urban'

    class Meta:
        model = Erf
        fields = ['id', 'cname', 'layer', 'type']


class HoldingParcelSerializer(ParcelBaseSerializer):
    """Serializer for Holding."""

    def get_layer(self, obj):
        return 'holding'

    def get_type(self, obj):
        return 'urban'

    class Meta:
        model = Holding
        fields = ['id', 'cname', 'layer', 'type']


class FarmPortionParcelSerializer(ParcelBaseSerializer):
    """Serializer for FarmPortion."""

    def get_layer(self, obj):
        return 'farm_portion'

    def get_type(self, obj):
        return 'rural'

    class Meta:
        model = FarmPortion
        fields = ['id', 'cname', 'layer', 'type']


class ParentFarmParcelSerializer(ParcelBaseSerializer):
    """Serializer for ParentFarm."""

    def get_layer(self, obj):
        return 'parent_farm'

    def get_type(self, obj):
        return 'rural'

    class Meta:
        model = ParentFarm
        fields = ['id', 'cname', 'layer', 'type']
