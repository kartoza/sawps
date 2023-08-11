"""Classes for upload helper.
"""
from datetime import datetime
from uuid import uuid4

from django.conf import settings
from django.db import models

FILE_STORAGE = 'species'


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


class UploadSpeciesCSV(models.Model):
    """Upload species csv model
    """

    property = models.ForeignKey(
        'property.Property',
        on_delete=models.CASCADE
    )

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        related_name='upload_session_uploader',
        blank=True,
        null=True,
    )

    token = models.UUIDField(
        default=uuid4,
        editable=False,
        null=True
    )

    uploaded_at = models.DateTimeField(
        default=datetime.now
    )

    processed = models.BooleanField(
        default=False
    )

    canceled = models.BooleanField(
        default=False
    )

    error_notes = models.TextField(
        blank=True,
        null=True
    )

    success_notes = models.TextField(
        blank=True,
        null=True
    )

    progress = models.CharField(
        max_length=200,
        default='',
        blank=True
    )

    process_file = models.FileField(
        upload_to=FILE_STORAGE,
        max_length=512,
        null=True
    )

    success_file = models.FileField(
        upload_to=FILE_STORAGE,
        null=True,
        max_length=512,
        blank=True
    )

    error_file = models.FileField(
        upload_to=FILE_STORAGE,
        null=True,
        max_length=512,
        blank=True
    )

    updated_file = models.FileField(
        upload_to=FILE_STORAGE,
        null=True,
        max_length=512,
        blank=True
    )

    class Meta:
        """Metaclass for project."""
        verbose_name_plural = 'Upload Sessions'
        verbose_name = 'Upload Session'

    def __str__(self):
        return str(self.token)
