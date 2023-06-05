import factory
from occurrence.models import OrganismQuantityType, SurveyMethod


class OrganismQuantityTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrganismQuantityType

    name = factory.Sequence(lambda n: "organism_quantity_type_%d" % n)
    sort_id = factory.Sequence(lambda n: n)
    
    
class SurveyMethodFactory(factory.django.DjangoModelFactory):
    """survey method factory"""

    class Meta:
        model = SurveyMethod

    name = factory.Sequence(lambda n: 'survey method {0}'.format(n))
    sort_id = factory.Sequence(lambda n: n)
