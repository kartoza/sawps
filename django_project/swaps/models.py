# coding=utf-8
"""
Species upload session model definition.

"""
import uuid
from django.conf import settings
from datetime import datetime
from django.db import models
FILE_STORAGE = 'species'


class UploadSession(models.Model):
    """Upload session model
    """

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        related_name='upload_session_uploader',
        blank=True,
        null=True,
    )

   
    token = models.UUIDField(
        default=uuid.uuid4,
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

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta class for project."""
        app_label = 'swaps'
        verbose_name_plural = 'Upload Sessions'
        verbose_name = 'Upload Session'

    def __str__(self):
        return str(self.token)
