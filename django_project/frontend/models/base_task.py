"""Base model for task.
"""
from django.db import models
from django.utils import timezone

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

    errors = models.TextField(
        null=True,
        blank=True
    )

    def task_on_started(self):
        """Initialize properties when task is started."""
        self.status = PROCESSING
        self.started_at = timezone.now()
        self.finished_at = None
        self.progress = 0
        self.progress_text = None
        self.save()

    def update_progress(self, current_progress, total_progress):
        """Update progress percentage."""
        if total_progress == 0:
            self.progress = 0
        else:
            self.progress = current_progress * 100 / total_progress
        self.save(update_fields=['progress'])
