import factory
from activity.models import ActivityType


class ActivtyTypeFactory(factory.django.DjangoModelFactory):
    """factory class for activity type models"""

    class Meta:
        model = ActivityType

    name = factory.Sequence(lambda n: f'Activity #{n}')
    recruitment = True
