import factory
from occurrence.models import SurveyMethod, OccurrenceStatus


class SurveyMethodFactory(factory.django.DjangoModelFactory):
    """survey method factory"""

    class Meta:
        model = SurveyMethod

    name = factory.Sequence(lambda n: 'survey method {0}'.format(n))
    sort_id = factory.Sequence(lambda n: n)


class OccurrenceStatusFactory(factory.django.DjangoModelFactory):
    """occurrence status factory"""

    class Meta:
        model = OccurrenceStatus

    name = factory.Sequence(lambda n: 'occurrence status {0}'.format(n))