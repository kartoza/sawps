from django.db import models
from django.conf import settings


class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='swaps_profile')

    picture = models.ImageField(
        upload_to='profile_pictures',
        null=True,
        blank=True
    )
