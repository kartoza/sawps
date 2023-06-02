import factory
from django.conf import settings
from django.contrib.auth import models


class GroupF(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Group
        django_get_or_create = ('id',)

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: 'name%s' % n)


class UserF(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('id',)

    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: 'username%s' % n)
    first_name = factory.Sequence(lambda n: 'first_name%s' % n)
    last_name = factory.Sequence(lambda n: 'last_name%s' % n)
    email = factory.Sequence(lambda n: 'email%s@example.com' % n)
    password = factory.PostGenerationMethodCall('set_password', 'password')
