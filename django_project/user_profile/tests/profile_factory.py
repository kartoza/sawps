import factory
from swaps.tests.models.account_factory import UserF
from user_profile.models import Profile


class ProfileF(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserF)
