"""Classes for Statistical R Model."""
from django.db import models
from django.conf import settings
from frontend.models.base_task import BaseTaskRequest
from uuid import uuid4


# model output types
NATIONAL_TREND = 'national_trend'
POPULATION_PER_PROVINCE = 'population_per_province'
PROVINCE_TREND = 'province_trend'
PROPERTY_TREND = 'property_trend'
POPULATION_PER_PROPERTY = 'population_per_property'


class StatisticalModel(models.Model):
    """Model that stores R code of statistical model."""

    taxon = models.ForeignKey(
        'species.Taxon',
        on_delete=models.CASCADE,
        unique=True
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


class StatisticalModelOutput(models.Model):
    """Output of statistical model."""

    OUTPUT_TYPE_CHOICES = (
        (NATIONAL_TREND, 'National Trend'),
        (POPULATION_PER_PROVINCE, 'Population Per Province'),
        (PROVINCE_TREND, 'Province Trend'),
        (PROPERTY_TREND, 'Property Trend'),
        (POPULATION_PER_PROPERTY, 'Population Per Property'),
    )

    model = models.ForeignKey(
        'frontend.StatisticalModel',
        on_delete=models.CASCADE
    )

    type = models.CharField(
        max_length=100,
        choices=OUTPUT_TYPE_CHOICES
    )
