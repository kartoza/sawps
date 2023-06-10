import factory
from regulatory_permit.models import DataUsePermission, DataUsePermissionChange


class DataUsePermissionFactory(factory.django.DjangoModelFactory):
    """Data use permission factory"""

    class Meta:
        model = DataUsePermission

    name = factory.Sequence(lambda n: 'data use permission %d' % n)
    description = factory.Sequence(
        lambda n: 'data use permission description %d' % n
    )


class DataUsePermissionChangeFactory(factory.django.DjangoModelFactory):
    """Datause permission change factory."""

    class Meta:
        model = DataUsePermissionChange

    date = factory.Faker('date')
    organisation = factory.SubFactory('stakeholder.factories.organisationFactory')
    user = factory.SubFactory('stakeholder.factories.userFactory')