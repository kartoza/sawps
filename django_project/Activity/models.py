from django.db import models


class ActivityType(models.Model):
    """activity type model"""

    name = models.CharField(max_length=150, unique=True)
    recruitment = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
