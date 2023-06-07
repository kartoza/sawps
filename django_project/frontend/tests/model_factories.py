"""Model factories for frontend."""
import factory

from django.contrib.auth import get_user_model
from frontend.models.context_layer import ContextLayer


class UserF(factory.django.DjangoModelFactory):
    """Factory for User model."""
    class Meta:
        """Meta class for UserF."""
        model = get_user_model()

    username = factory.Sequence(
        lambda n: f'username {n}'
    )


class ContextLayerF(factory.django.DjangoModelFactory):
    """Factory for ContextLayer Model."""
    class Meta:
        """Meta class Factory for ContextLayer Model."""
        model = ContextLayer
