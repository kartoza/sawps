"""Classes for upload helper."""
from django.db import models
from django.conf import settings
from uuid import uuid4


class DraftSpeciesUpload(models.Model):
    """Store draft of species upload data."""

    property = models.ForeignKey(
        'property.Property',
        on_delete=models.CASCADE
    )

    name = models.CharField(
        blank=False,
        null=False,
        max_length=256
    )

    upload_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    upload_date = models.DateTimeField()

    uuid = models.UUIDField(
        default=uuid4
    )

    taxon = models.ForeignKey(
        'species.Taxon',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    last_step = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    form_data = models.JSONField(
        default={},
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return f'{self.name}'
