from stakeholder.models import UserRoleType, UserTitle
import factory


class userRoleTypeFactory(factory.django.DjangoModelFactory):
    """factory class for user role type models"""

    class Meta:
        model = UserRoleType

    name = factory.Faker(
        "random_element", elements=("base user", "admin", "super user")
    )
    description = factory.Faker("text", max_nb_chars=200)

    
class userTitleFactory(factory.django.DjangoModelFactory):
    """factory class for user title models"""

    class Meta:
        model = UserTitle

    name = factory.Faker(
        'random_element', elements=('mr', 'mrs', 'miss', 'dr')
    )

    