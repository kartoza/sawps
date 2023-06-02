import factory
import property.models as PropertyModels


class PropertyTypeFactory(factory.django.DjangoModelFactory):
    """factory for PropertyType model"""

    class Meta:
        model = PropertyModels.PropertyType

    name = factory.Sequence(lambda n: 'PropertyType %d' % n)

    
class ProvinceFactory(factory.django.DjangoModelFactory):
    """Factory for Province"""

    class Meta:
        model = PropertyModels.Province

    name = factory.Sequence(lambda n: 'Province %d' % n)
