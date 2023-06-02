import factory
import property.models as PropertyModels


class ProvinceFactory(factory.django.DjangoModelFactory):
    """Factory for Province"""

    class Meta:
        model = PropertyModels.Province

    name = factory.Sequence(lambda n: "Province %d" % n)
