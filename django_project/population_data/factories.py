import factory
from population_data.models import CountMethod


class CountMethodFactory(factory.django.DjangoModelFactory):
    """count method factory"""

    class Meta:
        """meta"""

        model = CountMethod

    name = 'count method-1'
