import factory
from django.contrib.auth.models import Group
from sawps.models import ExtendedGroup, ExtendedGroupPermission


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



class ExtendedGroupPermissionF(factory.django.DjangoModelFactory):
    """
    Extended group model factory
    """
    name = factory.Sequence(
        lambda n: 'Permission %d' % n
    )

    class Meta:
        model = ExtendedGroupPermission
