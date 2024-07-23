"""Classes for Statistical R Model."""
from uuid import uuid4
from django.db import models
from django.db.models.signals import pre_delete, post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.functions import Lower
from frontend.models.base_task import BaseTaskRequest


# model output types
NATIONAL_TREND = 'national_trend'
PROVINCE_TREND = 'province_trend'
PROPERTY_TREND = 'property_trend'
SPECIES_PER_PROPERTY = 'species_per_property'
NATIONAL_GROWTH = 'national_growth'
PROVINCIAL_GROWTH = 'provincial_growth'
NATIONAL_GROWTH_CAT = 'national_growth_category'
NUM_PROPERTIES_PER_POP_SIZE_CAT = 'num_properties_per_pop_size_cat'
NUM_PROPERTIES_PER_DENSITY_CAT = 'num_properties_per_density_cat'
OTHER_DATA = 'other_data'
CUSTOM_AREA_AVAILABLE_GROWTH = 'custom_area_available_growth'

CACHED_OUTPUT_TYPES = [
    NATIONAL_TREND, PROVINCE_TREND,
    NATIONAL_GROWTH, PROVINCIAL_GROWTH,
    CUSTOM_AREA_AVAILABLE_GROWTH,
    NUM_PROPERTIES_PER_POP_SIZE_CAT,
    NUM_PROPERTIES_PER_DENSITY_CAT
]


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
    from frontend.tasks.generate_statistical_model import (
        check_affected_model_output
    )
    if instance.code and instance.id:
        check_affected_model_output.delay(instance.id, created)


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
        (PROVINCIAL_GROWTH, 'Provincial Growth'),
        (NATIONAL_GROWTH_CAT, 'National Growth Category'),
        (
            NUM_PROPERTIES_PER_POP_SIZE_CAT,
            'Number of Properties Per Population Size Category'
        ),
        (
            NUM_PROPERTIES_PER_DENSITY_CAT,
            'Number of Properties Per Density Category'
        ),
        (OTHER_DATA, 'Other Data')
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

    input_file = models.FileField(
        upload_to='statistical/input/%Y/%m/%d/',
        null=True,
        blank=True
    )

    output_file = models.FileField(
        upload_to='statistical/output/%Y/%m/%d/',
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

    def __str__(self) -> str:
        return f'{self.taxon}'

    def get_cache_key(self, output_type) -> str:
        taxon_name = slugify(self.taxon.scientific_name)
        return f'{str(self.uuid)}-{taxon_name}-{output_type}'


@receiver(pre_delete, sender=SpeciesModelOutput)
def species_model_output_pre_delete(sender,
                                    instance: SpeciesModelOutput,
                                    *args, **kwargs):
    from frontend.utils.statistical_model import (
        clear_species_model_output_cache
    )
    clear_species_model_output_cache(instance)


class OutputTypeCategoryIndexManager(models.Manager):
    """Manager class for output type category index."""

    def find_category_index(self, output_type, field_name):
        original_qs = self.annotate(val=Lower('value'))
        filter_type = f'{output_type}__{field_name}'
        qs = original_qs.filter(
            type=filter_type
        ).order_by('sort_index')
        if qs.exists():
            return qs
        return original_qs.filter(
            type=field_name
        ).order_by('sort_index')


class OutputTypeCategoryIndex(models.Model):
    """Define a sort index for output type of categories."""

    objects = OutputTypeCategoryIndexManager()

    type = models.CharField(
        max_length=255,
        help_text=(
            "The attribute name with/without the type name. "
            "e.g. pop_change_cat or national_growth__pop_change_cat"
        )
    )

    value = models.CharField(
        max_length=255,
        help_text=(
            "Part of category value. e.g. steady decrease"
        )
    )

    sort_index = models.IntegerField()
