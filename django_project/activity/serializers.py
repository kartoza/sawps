from rest_framework import serializers

from .models import ActivityType


class ActivityTypeSerializer(serializers.ModelSerializer):
    """Survey Method Serializer"""

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(ActivityTypeSerializer, self).__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    class Meta:
        model = ActivityType
        fields = '__all__'
