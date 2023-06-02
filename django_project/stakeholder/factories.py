from stakeholder import models as stakeholderModels
import factory


class userTitleFactory(factory.django.DjangoModelFactory):
    """factory class for user title models"""

    class Meta:
        model = stakeholderModels.UserTitle

    name = factory.Faker(
        'random_element', elements=('mr', 'mrs', 'miss', 'dr')
    )
