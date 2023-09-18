"""Serializer for road classes."""
from rest_framework import serializers
from frontend.models.road import Road


class RoadSearchSerializer(serializers.ModelSerializer):
    """Return id, name, bbox of property."""
    id = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    bbox = serializers.SerializerMethodField()

    def get_id(self, obj: Road):
        return f'property-{obj.id}'

    def get_type(self, obj: Road):
        return 'property'
    
    def get_bbox(self, obj: Road):
        if obj.geom is None:
            return []
        tf = obj.geom.transform(4326, clone=True)
        return list(tf.envelope.extent)

    class Meta:
        model = Road
        fields = [
            'id', 'type', 'name', 'bbox'
        ]
