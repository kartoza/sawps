"""Base model for task."""
from django.db import models
from datetime import datetime

# task statuses
PENDING = 'PENDING'
PROCESSING = 'PROCESSING'
DONE = 'DONE'
ERROR = 'ERROR'


class BaseTaskRequest(models.Model):
    """Abstract class for Base Task Request."""

    class Meta:
        """Meta class for abstract base task request."""
        abstract = True

    STATUS_CHOICES = (
        (PENDING, PENDING),
        (PROCESSING, PROCESSING),
        (DONE, DONE),
        (ERROR, ERROR)
    )

    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    finished_at = models.DateTimeField(
        null=True,
        blank=True
    )

    task_id = models.CharField(
        null=True,
        blank=True,
        max_length=256
    )

    progress = models.FloatField(
        null=True,
        blank=True
    )

    progress_text = models.TextField(
        null=True,
        blank=True
    )

    def task_on_started(self):
        """Initialize properties when task is started."""
        self.status = PROCESSING
        self.started_at = datetime.now()
        self.finished_at = None
        self.progress = 0
        self.progress_text = None
        self.save()
