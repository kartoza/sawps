# -*- coding: utf-8 -*-


"""Test factories for activity package.
"""
import factory
from activity.models import ActivityType


class ActivityTypeFactory(factory.django.DjangoModelFactory):
    """factory class for activity type models"""

    class Meta:
        model = ActivityType

    name = factory.Sequence(lambda n: f'Activity #{n}')
    recruitment = True
