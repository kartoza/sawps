import factory
from occurrence.models import OrganismQuantityType


class OrganismQuantityTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrganismQuantityType

    name = factory.Sequence(lambda n: "organism_quantity_type_%d" % n)
    sort_id = factory.Sequence(lambda n: n)
