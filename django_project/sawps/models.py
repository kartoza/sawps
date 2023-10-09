from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ExtendedGroup(models.Model):
    """
    Stores additional attributes for Django's built-in Group model.
    Related to :model:`auth.Group`.
    """

    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name='extended')

    description = models.TextField()

    def __str__(self):
        return self.group.name


@receiver(post_save, sender=Group)
def create_extended_group(sender, instance, created, **kwargs):
    """
    When a group is created, also create a ExtendedGroup
    """
    if (
            created and
            not ExtendedGroup.objects.filter(group=instance).exists()
    ):
        ExtendedGroup.objects.create(group=instance)


@receiver(post_save, sender=Group)
def save_extended_group(sender, instance, **kwargs):
    """
    Save the ExtendedGroup whenever a save event occurs
    """
    if ExtendedGroup.objects.filter(
        group_id=instance.id
    ).exists():
        instance.extended.save()
    else:
        ExtendedGroup.objects.create(group=instance)
