"""Serializer for stakeholder classes."""
from frontend.serializers.common import NameObjectBaseSerializer
from stakeholder.models import (
    Organisation,
    OrganisationUser
)


class OrganisationSerializer(NameObjectBaseSerializer):
    """Organisation Serializer."""

    class Meta:
        model = Organisation
        fields = NameObjectBaseSerializer.Meta.fields


class OrganisationUsersSerializer(NameObjectBaseSerializer):
    """OrganisationUsersSerializer"""

    class Meta:
        model = OrganisationUser
        fields = ("__all__")
