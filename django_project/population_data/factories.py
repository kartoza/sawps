import factory
from population_data.models import CountMethod, Month, NatureOfPopulation, PopulationCountAbstract, PopulationCount, PopulationCountPerActivity


class CountMethodFactory(factory.django.DjangoModelFactory):
    """Count method factory."""

    class Meta:
        """meta"""

        model = CountMethod

    name = 'count method-1'


class MonthFactory(factory.django.DjangoModelFactory):
    """Month factory."""

    class Meta:
        model = Month

    name = factory.Sequence(lambda n: 'month-{0}'.format(n))
    sort_order = factory.Sequence(lambda n: n)


class NatureOfPopulationFactory(factory.django.DjangoModelFactory):
    """Nature of the population factory."""

    class Meta:
        model = NatureOfPopulation

    name = factory.Sequence(lambda n: 'nature of population-{0}'.format(n))
    extensive = True


class PopulationCountAbstractFactory(factory.django.DjangoModelFactory):
    """Population count abstract factory."""
    class Meta:
        model = PopulationCountAbstract
        abstract = True

    year = factory.Faker('date')
    owned_species = factory.SubFactory('species.factories.OwnedSpeciesFactory')
    total = factory.Faker('random_int')
    adult_male = factory.Faker('random_int')
    adult_female = factory.Faker('random_int')
    month = factory.SubFactory(MonthFactory)
    juvenile_male = factory.Faker('random_int')
    juvenile_female = factory.Faker('random_int')

    @factory.post_generation
    def owned_species(self, create, extracted, **kwargs):
        """Add activity type to population count per activity."""
        if not create:
            return
        if extracted:
            for owned_species in extracted:
                self.owned_species.add(owned_species)



class PopulationCountFactory(PopulationCountAbstractFactory):
    """Population count factory."""
    class Meta:
        model = PopulationCount

    sub_adult_total = factory.Faker('random_int')
    sub_adult_male = factory.Faker('random_int')
    sub_adult_female = factory.Faker('random_int')
    juvenile_total = factory.Faker('random_int')
    pride = factory.Faker('random_int')


class PopulationCountPerActivityFactory(PopulationCountAbstractFactory):
    """Population count per activity factory."""
    class Meta:
        model = PopulationCountPerActivity
    
    founder_population = True
    reintroduction_source = factory.Sequence(lambda n: 'reintroduction source-{0}'.format(n))
    permit_number = factory.Faker('random_int')

    @factory.post_generation
    def activity_type(self, create, extracted, **kwargs):
        """Add activity type to population count per activity."""
        if not create:
            return
        if extracted:
            for activity_type in extracted:
                self.activity_type.add(activity_type)
