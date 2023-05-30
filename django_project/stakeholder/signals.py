from django.db.models.signals import post_delete
from django.dispatch import receiver
from stakeholder.models import UserProfile


@receiver(post_delete, sender=UserProfile)
def delete_associated_user(sender, instance, **kwargs):
    """delete associated user when user profile is deleted"""
    if instance.user:
        instance.user.delete()
