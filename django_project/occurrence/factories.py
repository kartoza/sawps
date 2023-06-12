import factory
from occurrence.models import SurveyMethod, BasisOfRecord, SamplingSizeUnit, OccurrenceStatus, OrganismQuantityType, Occurrence


class OrganismQuantityTypeFactory(factory.django.DjangoModelFactory):
    """Organism quantity type factory. """
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


class OccurrenceFactory(factory.django.DjangoModelFactory):
    """Occurrence factory."""
    class Meta:
        model = Occurrence

    individual_count = factory.Faker('random_int')
    organism_quantity = factory.Faker('random_int')
    sampling_size_value = factory.Faker('pyfloat')
    datetime = factory.Faker('date_time')
    owner_institution_code = factory.sequence(lambda n: 'owner_institution_code_{0}'.format(n))
    coordinates_uncertainty_m = factory.Faker('random_int')
    geometry = """{"type": "Point", "coordinates": [30.0, 10.0]}"""
    basis_of_record = factory.SubFactory(BasisOfRecordFactory)
    ogranism_quantity_type = factory.SubFactory(OrganismQuantityTypeFactory)
    occurrence_status = factory.SubFactory(OccurrenceStatusFactory)
    sampling_size_unit = factory.SubFactory(SamplingSizeUnitFactory)
    survey_method = factory.SubFactory(SurveyMethodFactory)
    organisation = factory.SubFactory('stakeholder.factories.organisationFactory')
