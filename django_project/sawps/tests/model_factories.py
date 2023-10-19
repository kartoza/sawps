import factory
from django.contrib.auth.models import Group
from sawps.models import ExtendedGroup


class GroupF(factory.django.DjangoModelFactory):
    """
    Group model factory
    """
    class Meta:
        model = Group

    name = factory.Sequence(
        lambda n: 'Group name %d' % n
    )


class ExtendedGroupF(factory.django.DjangoModelFactory):
    """
    Extended group model factory
    """
    description = factory.Sequence(
        lambda n: 'Description %d' % n
    )
    group = factory.SubFactory(GroupF)

    class Meta:
        model = ExtendedGroup
