import factory
from regulatory_permit import models as regulatoryPermitModels

class dataUsePermissionFactory(factory.django.DjangoModelFactory):
    """data use permission factory"""

    class Meta:
        model = regulatoryPermitModels.dataUsePermission

    name = 'Data use permission'
    description = 'Data use permission description'


class dataUsePermissionChangeFactory(factory.django.DjangoModelFactory):
    """data use permission change factory"""

    class Meta:
        model = regulatoryPermitModels.dataUsePermissionChange

    date = '2017-01-01'
    organization = factory.SubFactory('stakeholder.factories.OrganizationFactory')
    user = factory.SubFactory('stakeholder.factories.userProfileFactory')