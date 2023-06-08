import factory
from property.models import PropertyType, Province, OwnershipStatus


class PropertyTypeFactory(factory.django.DjangoModelFactory):
    """Factory for PropertyType model."""

    class Meta:
        model = PropertyType

    name = factory.Sequence(lambda n: 'PropertyType %d' % n)


class ProvinceFactory(factory.django.DjangoModelFactory):
    """Factory for Province."""

    class Meta:
        model = Province

    name = factory.Sequence(lambda n: 'Province %d' % n)


class OwnershipStatusFactory(factory.django.DjangoModelFactory):
    """Factory for OwnershipStatus."""

    class Meta:
        model = OwnershipStatus

    name = factory.Sequence(lambda n: 'OwnershipStatus_%d' % n)