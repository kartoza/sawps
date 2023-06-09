import factory
from property.models import PropertyType, Province, OwnershipStatus, Property


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



class PropertyFactory(factory.django.DjangoModelFactory):
    """Property factory."""

    class Meta:
        model = Property

    name = factory.Sequence(lambda n: 'property_%d' % n)
    property_type = factory.SubFactory(PropertyTypeFactory)
    province = factory.SubFactory(ProvinceFactory)
    ownership_status = factory.SubFactory(OwnershipStatusFactory)
    property_size_ha = 200
    organization = factory.SubFactory('stakeholder.factories.organizationFactory')
    area_available = 150
    geometry = 'POLYGON ((-123.456 48.123, -123.456 48.456, -123.123 48.456, -123.456 48.123))'
    owner_email = factory.Faker('email')
    created_by = factory.SubFactory('stakeholder.factories.userFactory')
    created_at = factory.Faker('date_time')
