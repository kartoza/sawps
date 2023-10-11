# -*- coding: utf-8 -*-


"""Models for activity package.
"""
from django.db import models


class ActivityType(models.Model):
    """activity type model"""

    name = models.CharField(max_length=150, unique=True)
    recruitment = models.BooleanField(null=True, blank=True)
    colour = models.CharField(max_length=20, null=True, blank=True)
    export_fields = models.JSONField(
        default=list,
        help_text=(
            'Fields that will be taken from Annual Population Per Activity table '
            'when exporting Activity Report. Input as Array e.g. ["intake_permit", "translocation_destination"]'
        )
    )

    def __str__(self):
        return self.name

    @classmethod
    def get_all_activities(cls):
        return list(cls.objects.values_list('name', flat=True).order_by('name'))

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
