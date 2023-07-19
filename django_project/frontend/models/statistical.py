"""Classes for Statistical R Model."""
from django.db import models
from django.conf import settings
from frontend.models.base_task import BaseTaskRequest
from uuid import uuid4


class StatisticalModel(models.Model):
    """Model that stores R code of statistical model."""

    taxon = models.ForeignKey(
        'species.Taxon',
        on_delete=models.CASCADE
    )

    name = models.CharField(
        blank=False,
        null=False,
        max_length=256
    )

    code = models.TextField(
        null=True,
        blank=True
    )

    is_valid = models.BooleanField(
        null=True
    )

    last_error = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return f'{self.taxon} - {self.name}'


class StatisticalTaskRequest(BaseTaskRequest):
    """Task to run statistical R Model."""

    request_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    organisation = models.ForeignKey(
        'stakeholder.Organisation', on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to='statistical/%Y/%m/%d/',
        null=True,
        blank=True
    )

    response = models.JSONField(
        default=dict,
        null=True,
        blank=True
    )

    uuid = models.UUIDField(
        default=uuid4
    )

    taxon = models.ForeignKey(
        'species.Taxon',
        on_delete=models.CASCADE
    )

    statistical_model = models.ForeignKey(
        'frontend.StatisticalModel',
        on_delete=models.CASCADE
    )

    is_success = models.BooleanField(
        null=True
    )

    return_code = models.IntegerField(
        null=True,
        blank=True
    )

    error = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return str(self.uuid)

    def reset(self):
        if self.image:
            self.image.delete()
        self.image = None
        self.response = None
        self.is_success = None
        self.return_code = None
        self.error = None
        self.save()
