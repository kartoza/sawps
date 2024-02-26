"""Serializers for ContextLayer."""
from rest_framework import serializers
from frontend.models.context_layer import ContextLayer, ContextLayerLegend


class ContextLayerLegendSerializer(serializers.ModelSerializer):
    """Legend serializer."""
    class Meta:
        model = ContextLayerLegend
        fields = ['name', 'colour']


class ContextLayerSerializer(serializers.ModelSerializer):
    """ContextLayer serializer."""
    legends = serializers.SerializerMethodField()

    def get_legends(self, obj: ContextLayer):
        legends = obj.contextlayerlegend_set.all().order_by('name')
        return ContextLayerLegendSerializer(
            legends,
            many=True
        ).data

    class Meta:
        """Meta class for serializer."""
        model = ContextLayer
        fields = ['id', 'name', 'layer_names', 'legends', 'description']
