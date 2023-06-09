import factory
from property.models import PropertyType, Province, OwnershipStatus, Property, ParcelType, Parcel


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
    organisation = factory.SubFactory('stakeholder.factories.organisationFactory')
    area_available = 150
    geometry = 'MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40)),((20 35, 45 20, 30 5, 10 10, 10 30, 20 35),(30 20, 20 25, 20 15, 30 20)))'
    owner_email = factory.Faker('email')
    created_by = factory.SubFactory('stakeholder.factories.userFactory')
    created_at = factory.Faker('date_time')


class ParcelTypeFactory(factory.django.DjangoModelFactory):
    """Factory for ParcelType."""

    class Meta:
        model = ParcelType

    name = factory.Sequence(lambda n: 'ParcelType_%d' % n)

class ParcelFactory(factory.django.DjangoModelFactory):
    """Factory for Parcel."""

    class Meta:
        model = Parcel

    sg_number = factory.Sequence(lambda n: 'SG_%d' % n)
    year = factory.Sequence(lambda n: '201%d-10-10' % n)
    parcel_type = factory.SubFactory(ParcelTypeFactory)
    property = factory.SubFactory(PropertyFactory)