from rest_framework import serializers
from activity.models import (
    ActivityType
)


class ActivityTypeSerializer(serializers.ModelSerializer):
    """ActivityType serializer"""

    class Meta():
        model = ActivityType
        fields = ['id', 'name']
