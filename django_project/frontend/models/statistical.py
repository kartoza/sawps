"""Classes for Statistical R Model."""
from uuid import uuid4
from django.db import models
from django.db.models.signals import pre_delete, post_save, post_delete
from django.dispatch import receiver
from frontend.models.base_task import BaseTaskRequest


# model output types
NATIONAL_TREND = 'national_trend'
PROVINCE_TREND = 'province_trend'
PROPERTY_TREND = 'property_trend'
SPECIES_PER_PROPERTY = 'species_per_property'
NATIONAL_GROWTH = 'national_growth'
PROVINCIAL_GROWTH = 'provincial_growth'


class StatisticalModel(models.Model):
    """Model that stores R code of statistical model."""

    taxon = models.ForeignKey(
        'species.Taxon',
        on_delete=models.CASCADE,
        unique=True,
        blank=True,
        null=True,
    )

    name = models.CharField(
        blank=False,
        null=False,
        max_length=256
    )

    code = models.TextField(
        null=False,
        blank=False
    )

    def __str__(self) -> str:
        return f'{self.taxon} - {self.name}'


@receiver(post_save, sender=StatisticalModel)
def statistical_model_post_create(sender, instance: StatisticalModel,
                                  created, *args, **kwargs):
    from frontend.tasks.start_plumber import (
        start_plumber_process
    )
    from frontend.utils.statistical_model import (
        clear_statistical_model_output_cache
    )
    if not created:
        clear_statistical_model_output_cache(instance.taxon)
    if instance.code:
        # respawn Plumber API
        start_plumber_process.apply_async(queue='plumber')


@receiver(pre_delete, sender=StatisticalModel)
def statistical_model_pre_delete(sender, instance: StatisticalModel,
                                 *args, **kwargs):
    from frontend.utils.statistical_model import (
        clear_statistical_model_output_cache
    )
    clear_statistical_model_output_cache(instance.taxon)


@receiver(post_delete, sender=StatisticalModel)
def statistical_model_post_delete(sender, instance: StatisticalModel,
                                  *args, **kwargs):
    from frontend.tasks.start_plumber import (
        start_plumber_process
    )
    # respawn Plumber API
    start_plumber_process.apply_async(queue='plumber')


class StatisticalModelOutput(models.Model):
    """Output of statistical model."""

    OUTPUT_TYPE_CHOICES = (
        (NATIONAL_TREND, 'National Trend'),
        (PROVINCE_TREND, 'Province Trend'),
        (PROPERTY_TREND, 'Property Trend'),
        (SPECIES_PER_PROPERTY, 'Species Per Property'),
        (NATIONAL_GROWTH, 'National Growth'),
        (PROVINCIAL_GROWTH, 'Provincial Growth')
    )

    model = models.ForeignKey(
        'frontend.StatisticalModel',
        on_delete=models.CASCADE
    )

    type = models.CharField(
        max_length=100,
        choices=OUTPUT_TYPE_CHOICES
    )

    variable_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )


class SpeciesModelOutput(BaseTaskRequest):
    """Store statistical model output for a species."""

    model = models.ForeignKey(
        'frontend.StatisticalModel',
        on_delete=models.CASCADE
    )

    taxon = models.ForeignKey(
        'species.Taxon',
        on_delete=models.CASCADE
    )

    output_file = models.FileField(
        upload_to='statistical/%Y/%m/%d/',
        null=True,
        blank=True
    )

    uuid = models.UUIDField(
        default=uuid4
    )

    is_latest = models.BooleanField(
        default=False
    )

    generated_on = models.DateTimeField(
        null=True,
        blank=True
    )

    is_outdated = models.BooleanField(
        default=False
    )

    outdated_since = models.DateTimeField(
        null=True,
        blank=True
    )
