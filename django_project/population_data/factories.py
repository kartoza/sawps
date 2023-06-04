import factory
from population_data.models import NatureOfPopulation

class NatureOfPopulationFactory(factory.django.DjangoModelFactory):
    """
    nature of the population factory.
    """
    class Meta:
        model = NatureOfPopulation

    name = factory.Sequence(lambda n: 'nature of population-{0}'.format(n))
    extensive = True