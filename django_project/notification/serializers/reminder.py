from rest_framework import serializers
from notification.models import Reminder


class ReminderSerializer(serializers.ModelSerializer):
    """Serializer for reminder"""

    class Meta:
        model = Reminder
        fields = ['id', 'title', 'date', 'text', 'status']
