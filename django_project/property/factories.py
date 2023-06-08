import factory
import property.models as PropertyModels


class PropertyTypeFactory(factory.django.DjangoModelFactory):
    """Factory for PropertyType model."""

    class Meta:
        model = PropertyModels.PropertyType

    name = factory.Sequence(lambda n: 'PropertyType %d' % n)


class ProvinceFactory(factory.django.DjangoModelFactory):
    """Factory for Province."""

    class Meta:
        model = PropertyModels.Province

    name = factory.Sequence(lambda n: 'Province %d' % n)


class ParcelTypeFactory(factory.django.DjangoModelFactory):
    """Factory for ParcelType."""

    class Meta:
        model = PropertyModels.ParcelType

    name = factory.Sequence(lambda n: 'ParcelType_%d' % n)

class ParcelFactory(factory.django.DjangoModelFactory):
    """Factory for Parcel."""

    class Meta:
        model = PropertyModels.Parcel

    sg_number = factory.Sequence(lambda n: 'SG_%d' % n)
    year = factory.Sequence(lambda n: '201%d-10-10' % n)
    parcel_type = factory.SubFactory(ParcelTypeFactory)