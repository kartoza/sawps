from stakeholder import models as stakeholderModels
import factory


class userRoleTypeFactory(factory.django.DjangoModelFactory):
    """factory class for user role type models"""

    class Meta:
        model = stakeholderModels.UserRoleType

    name = factory.Faker(
        "random_element", elements=("base user", "admin", "super user")
    )
    description = factory.Faker("text", max_nb_chars=200)
