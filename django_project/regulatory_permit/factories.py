import factory
import regulatory_permit.models as regulatoryPermitModels


class DataUsePermissionFactory(factory.django.DjangoModelFactory):
    """data use permission factory"""

    class Meta:
        model = regulatoryPermitModels.DataUsePermission

    name = factory.Sequence(lambda n: 'data use permission %d' % n)
    description = factory.Sequence(
        lambda n: 'data use permission description %d' % n
    )
