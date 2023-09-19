"""Serializer for place classes."""
from rest_framework import serializers
from frontend.models.places import (
    PlaceNameSmallScale,
    PlaceNameLargerScale,
    PlaceNameLargestScale,
    PlaceNameMidScale
)


class PlaceBaseSearchSerializer(serializers.ModelSerializer):
    """Return id, name, bbox of place."""
    id = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    bbox = serializers.SerializerMethodField()

    def get_id(self, obj):
        return f'{self.get_type(obj)}-{obj.id}'

    def get_type(self, obj):
        raise NotImplementedError('get_type')

    def get_bbox(self, obj):
        if obj.geom is None:
            return []
        tf = obj.geom.transform(4326, clone=True)
        return list(tf.extent)


class PlaceSmallScaleSearchSerializer(PlaceBaseSearchSerializer):

    def get_type(self, obj):
        return 'place-name-small-scale'

    class Meta:
        model = PlaceNameSmallScale
        fields = [
            'id', 'type', 'name', 'bbox', 'fclass'
        ]


class PlaceLargerScaleSearchSerializer(PlaceBaseSearchSerializer):

    def get_type(self, obj):
        return 'place-name-larger-scale'

    class Meta:
        model = PlaceNameLargerScale
        fields = [
            'id', 'type', 'name', 'bbox', 'fclass'
        ]


class PlaceLargestScaleSearchSerializer(PlaceBaseSearchSerializer):

    def get_type(self, obj):
        return 'place-name-largest-scale'

    class Meta:
        model = PlaceNameLargestScale
        fields = [
            'id', 'type', 'name', 'bbox', 'fclass'
        ]


class PlaceMidScaleSearchSerializer(PlaceBaseSearchSerializer):

    def get_type(self, obj):
        return 'place-name-mid-scale'

    class Meta:
        model = PlaceNameMidScale
        fields = [
            'id', 'type', 'name', 'bbox', 'fclass'
        ]
