import factory
from occurrence.models import SurveyMethod, BasisOfRecord, SamplingSizeUnit, OccurrenceStatus, OrganismQuantityType


class OrganismQuantityTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrganismQuantityType

    name = factory.Sequence(lambda n: "organism_quantity_type_%d" % n)
    sort_id = factory.Sequence(lambda n: n)


class SurveyMethodFactory(factory.django.DjangoModelFactory):
    """Survey method factory."""

    class Meta:
        model = SurveyMethod

    name = factory.Sequence(lambda n: 'survey method {0}'.format(n))
    sort_id = factory.Sequence(lambda n: n)


class OccurrenceStatusFactory(factory.django.DjangoModelFactory):
    """Occurrence status factory."""

    class Meta:
        model = OccurrenceStatus

    name = factory.Sequence(lambda n: 'occurrence status {0}'.format(n))

    
class BasisOfRecordFactory(factory.django.DjangoModelFactory):
    """Basis of record factory."""

    class Meta:
        model = BasisOfRecord

    name = factory.Sequence(lambda n: 'basis of record {0}'.format(n))
    sort_id = factory.Sequence(lambda n: n)

    
class SamplingSizeUnitFactory(factory.django.DjangoModelFactory):
    """Sampling size unit factory."""

    class Meta:
        model = SamplingSizeUnit

    unit = factory.Faker('random_choices', elements='cm')
