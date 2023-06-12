import factory
from django.conf import settings
from notification.models import Reminder


class ReminderF(factory.django.DjangoModelFactory):
    class Meta:
        model = Reminder
        django_get_or_create = ('id',)

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: 'title%s' % n)
    text = factory.Sequence(lambda n: 'text%s' % n)
    status = factory.Sequence(lambda n: 'status%s' % n)
