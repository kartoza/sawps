"""Serializer for stakeholder classes."""
from frontend.serializers.common import NameObjectBaseSerializer
from stakeholder.models import (
    Organisation
)


class OrganisationSerializer(NameObjectBaseSerializer):
    """Organisation Serializer."""

    class Meta:
        model = Organisation
        fields = NameObjectBaseSerializer.Meta.fields
