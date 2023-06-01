import factory
import property.models as PropertyModels


class PropertyTypeFactory(factory.django.DjangoModelFactory):
    """factory for PropertyType model"""

    class Meta:
        model = PropertyModels.PropertyType

    name = factory.Sequence(lambda n: 'PropertyType %d' % n)
