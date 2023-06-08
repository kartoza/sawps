import factory
from population_data.models import CountMethod, Month, NatureOfPopulation


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
