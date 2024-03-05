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


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    organisation = serializers.StringRelatedField()
    date = serializers.DateTimeField(format='%Y-%m-%d %I:%M %p')
    can_remove = serializers.SerializerMethodField()

    def get_can_remove(self, obj: Reminders):
        if obj.type == Reminders.EVERYONE:
            user = self.context['user']
            # only creator can remove this notification
            return user == obj.user
        return True

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
            'email_sent',
            'can_remove'
        ]


class OrganisationMemberSerializer(serializers.ModelSerializer):
    """Organisation member serializer."""
    user_id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    is_manager = serializers.SerializerMethodField()

    def get_user_id(self, obj: OrganisationUser):
        return obj.user.id

    def get_name(self, obj: OrganisationUser):
        return obj.full_name.strip() if obj.full_name else ''

    def get_is_manager(self, obj: OrganisationUser):
        manager_ids = (
            self.context['manager_ids'] if 'manager_ids' in self.context else
            []
        )
        if obj.user.is_superuser:
            return True
        return obj.user.id in manager_ids

    class Meta:
        model = OrganisationUser
        fields = [
            'user_id',
            'name',
            'is_manager'
        ]
