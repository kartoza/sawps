from datetime import datetime
from django.db import models


class Reminder(models.Model):
    """ Reminder notification model"""

    STATUS_CHOISES = (
        ('active', 'Active'),
        ('draft', 'Draft')
    )

    title = models.CharField(
        max_length=200,
        default='',
        null=False,
        help_text='Reminder title'
    )

    date = models.DateTimeField(
        default=datetime.now
    )

    text = models.TextField(
        null=True,
        blank=True,
        help_text='Reminder text'
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOISES,
        blank=True,
        null=True,
    )
