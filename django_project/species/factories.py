import factory
from species.models import ManagementStatus


class ManagementStatusFactory(factory.django.DjangoModelFactory):
    """ management status factory """

    class Meta:
        model = ManagementStatus

    name = factory.Sequence(lambda n: 'management status_%d' % n)