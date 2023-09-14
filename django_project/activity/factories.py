"""Test factories for activity package.
"""
import random

import factory
from activity.models import ActivityType

activity_list = [
    "Planned translocation", "Planned euthanasia", "Planned hunt/cull",
    "Unplanned/illegal hunting", "Unplanned/natural deaths",
]


class ActivityTypeFactory(factory.django.DjangoModelFactory):
    """Factory class for activity type models."""

    class Meta:
        model = ActivityType

    name = factory.LazyFunction(lambda: generate_unique_name(activity_list))
    recruitment = True


def generate_unique_name(activity_list) -> str:
    """Return activity name"""
    while True:
        name = random.choice(activity_list)
        if not ActivityType.objects.filter(name=name).exists():
            return name
