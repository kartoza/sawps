from stakeholder import models as stakeholderModels
import factory
import datetime
from django.contrib.auth.models import User


class userTitleFactory(factory.django.DjangoModelFactory):
    """factory class for user title models"""

    class Meta:
        model = stakeholderModels.UserTitle

    name = factory.Faker(
        'random_element', elements=('mr', 'mrs', 'miss', 'dr')
    )


class userRoleTypeFactory(factory.django.DjangoModelFactory):
    """factory class for user role type models"""

    class Meta:
        model = stakeholderModels.UserRoleType

    name = factory.Faker(
        'random_element', elements=('base user', 'admin', 'super user')
    )
    description = factory.Faker('text', max_nb_chars=200)


class loginStatusFactory(factory.django.DjangoModelFactory):
    """factory class for login status models"""

    class Meta:
        model = stakeholderModels.LoginStatus

    name = factory.Faker(
        'random_element', elements=('logged in', 'logged out')
    )


class userFactory(factory.django.DjangoModelFactory):
    """factory class for user models"""

    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')
    email = factory.Faker('email')


class userProfileFactory(factory.django.DjangoModelFactory):
    """factory class for user profile model"""

    class Meta:
        model = stakeholderModels.UserProfile

    # we aren't using profile = None
    # described here https://factoryboy.readthedocs.io/
    # en/stable/recipes.html#example-django-s-profile
    user = factory.SubFactory('stakeholder.factories.userFactory')

    title_id = factory.SubFactory('stakeholder.factories.userTitleFactory')
    cell_number = factory.Faker('random_int', min=10000, max=99999)
    user_role_type_id = factory.SubFactory(
        'stakeholder.factories.userRoleTypeFactory'
    )


class userLoginFactory(factory.django.DjangoModelFactory):
    """factory class for user login model"""

    class Meta:
        model = stakeholderModels.UserLogin

    user = factory.SubFactory('stakeholder.factories.userProfileFactory')
    login_status_id = factory.SubFactory(
        'stakeholder.factories.loginStatusFactory'
    )
    datetime = factory.Faker(
        'date_time_this_year', tzinfo=datetime.timezone.utc
    )
    ip_address = factory.Faker('ipv4')


class OrganizationFactory(factory.django.DjangoModelFactory):
    """factory class for organization model"""

    class Meta:
        model = stakeholderModels.Organization

    name = factory.Faker('company')
    data_use_permission = factory.SubFactory(
        'regulatory_permit.factories.dataUsePermissionFactory'
    )


class OrganizationRepresentativeFactory(factory.django.DjangoModelFactory):
    """factory class for organization representative model"""

    class Meta:
        model = stakeholderModels.OrganizationRepresentatives

    organization = factory.SubFactory(
        'stakeholder.factories.OrganizationFactory'
    )
    user = factory.SubFactory('stakeholder.factories.userFactory')


class OrganizationUserFactory(factory.django.DjangoModelFactory):
    """factory class for organization user model"""

    class Meta:
        model = stakeholderModels.OrganizationRepresentatives

    organization = factory.SubFactory(
        'stakeholder.factories.OrganizationFactory'
    )
    user = factory.SubFactory('stakeholder.factories.userFactory')
