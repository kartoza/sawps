from stakeholder.models import UserRoleType, UserTitle, LoginStatus, UserProfile
import factory
from django.contrib.auth.models import User


class userRoleTypeFactory(factory.django.DjangoModelFactory):
    """Factory class for user role type models."""

    class Meta:
        model = UserRoleType

    name = factory.Faker(
        'random_element', elements=('base user', 'admin', 'super user')
    )
    description = factory.Faker('text', max_nb_chars=200)


class loginStatusFactory(factory.django.DjangoModelFactory):
    """Factory class for login status models."""

    class Meta:
        model = LoginStatus

    name = factory.Faker(
        'random_element', elements=('logged in', 'logged out')
    )


class userTitleFactory(factory.django.DjangoModelFactory):
    """Factory class for user title models."""

    class Meta:
        model = UserTitle

    name = factory.Faker(
        'random_element', elements=('mr', 'mrs', 'miss', 'dr')
    )


class userFactory(factory.django.DjangoModelFactory):
    """Factory class for user models."""

    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')
    email = factory.Faker('email')


class userProfileFactory(factory.django.DjangoModelFactory):
    """Factory class for user profile model."""

    class Meta:
        model = UserProfile

    user = factory.SubFactory('stakeholder.factories.userFactory')
    title_id = factory.SubFactory('stakeholder.factories.userTitleFactory')
    cell_number = factory.Faker('random_int', min=10000, max=99999)
    user_role_type_id = factory.SubFactory(
        'stakeholder.factories.userRoleTypeFactory'
    )
