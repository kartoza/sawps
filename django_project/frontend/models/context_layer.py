"""Context Layers with mapping table to tegola layers."""
from django.db import models


class ContextLayer(models.Model):
    """A model for the context layer."""

    name = models.CharField(
        max_length=512
    )

    is_static = models.BooleanField(
        default=True,
    )

    layer_names = models.JSONField(
        default=[],
        blank=True
    )
