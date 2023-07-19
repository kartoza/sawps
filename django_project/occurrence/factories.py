import factory
from occurrence.models import (
    SurveyMethod,
    SamplingSizeUnit,
)


class SurveyMethodFactory(factory.django.DjangoModelFactory):
    """Survey method factory."""

    class Meta:
        model = SurveyMethod

    name = factory.Sequence(lambda n: 'survey method {0}'.format(n))
    sort_id = factory.Sequence(lambda n: n)


class SamplingSizeUnitFactory(factory.django.DjangoModelFactory):
    """Sampling size unit factory."""
    class Meta:
        model = SamplingSizeUnit

    unit = factory.Faker('random_choices', elements='cm')
