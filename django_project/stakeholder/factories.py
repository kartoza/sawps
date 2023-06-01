from stakeholder import models as stakeholderModels
import factory


class loginStatusFactory(factory.django.DjangoModelFactory):
    """factory class for login status models"""

    class Meta:
        model = stakeholderModels.LoginStatus

    name = factory.Faker(
        "random_element", elements=("logged in", "logged out")
    )
