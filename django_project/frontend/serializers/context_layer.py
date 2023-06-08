"""Serializers for ContextLayer."""
from rest_framework import serializers
from frontend.models.context_layer import ContextLayer


class ContextLayerSerializer(serializers.ModelSerializer):
    """ContextLayer serializer."""
    class Meta:
        """Meta class for serializer."""
        model = ContextLayer
        fields = ['id', 'name', 'layer_names']
