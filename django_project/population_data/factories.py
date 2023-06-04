import factory
from population_data.models import Month

class MonthFactory(factory.django.DjangoModelFactory):
    """ month factory """
    class Meta:
        model = Month

    name = factory.Sequence(lambda n: 'month-{0}'.format(n))
    sorid = factory.Sequence(lambda n: n)