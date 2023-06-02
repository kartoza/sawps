import factory
import occurrence.models as OccurrenceModels


class SurveyMethodFactory(factory.django.DjangoModelFactory):
    """survey method factory"""

    class Meta:
        model = OccurrenceModels.SurveyMethod

    name = factory.Sequence(lambda n: 'survey method {0}'.format(n))
    sort_id = factory.Sequence(lambda n: n)
