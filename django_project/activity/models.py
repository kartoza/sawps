# -*- coding: utf-8 -*-


"""Models for activity package.
"""
from django.db import models


class ActivityType(models.Model):
    """activity type model"""

    name = models.CharField(max_length=150, unique=True)
    recruitment = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
