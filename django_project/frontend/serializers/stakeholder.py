"""Serializer for stakeholder classes."""
from frontend.serializers.common import NameObjectBaseSerializer
from stakeholder.models import (
    Organisation,
    OrganisationUser,
    Reminders
)
from rest_framework import serializers


class OrganisationSerializer(NameObjectBaseSerializer):
    """Organisation Serializer."""

    class Meta:
        model = Organisation
        fields = '__all__'


class OrganisationUsersSerializer(NameObjectBaseSerializer):
    """OrganisationUsersSerializer"""

    class Meta:
        model = OrganisationUser
        fields = ("__all__")



class ReminderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    organisation = serializers.StringRelatedField()
    date = serializers.DateTimeField(format='%Y-%m-%d %I:%M %p')

    class Meta:
        model = Reminders
        fields = [
            'id',
            'title',
            'reminder',
            'user',
            'organisation',
            'status',
            'date',
            'type',
            'email_sent'
        ]
