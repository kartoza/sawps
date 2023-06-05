import factory
from occurrence.models import SurveyMethod, BasisOfRecord


class SurveyMethodFactory(factory.django.DjangoModelFactory):
    """survey method factory"""

    class Meta:
        model = SurveyMethod

    name = factory.Sequence(lambda n: 'survey method {0}'.format(n))
    sort_id = factory.Sequence(lambda n: n)


class BasisOfRecordFactory(factory.django.DjangoModelFactory):
    """basis of record factory"""

    class Meta:
        model = BasisOfRecord

    name = factory.Sequence(lambda n: 'basis of record {0}'.format(n))
    sort_id = factory.Sequence(lambda n: n)