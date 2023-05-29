from django.db import models

class ActivityType(models.Model):
    """activity type model"""
    activity_types = [('planned translocation','Planned translocation'),('planned hunt/cull','Planned hunt/cull'),('unplanned/natural deaths','Unplanned/natural deaths'),('planned euthanasia','Planned euthanasia'),('unplanned/illegal hunting','Unplanned/illegal hunting')]
    name = models.CharField(max_length=150, unique=True, choices=activity_types)
    recruitment = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'