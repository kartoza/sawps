# -*- coding: utf-8 -*-

"""Place tables from layer schema.

"""
from django.contrib.gis.db import models


class PlaceBase(models.Model):
    """Base Model for Place Tables."""

    id = models.AutoField(primary_key=True)

    geom = models.PointField(
        null=True,
        srid=3857
    )

    fclass = models.CharField(
        max_length=28,
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_index=True
    )

    class Meta:
        """Meta class for PlaceBase."""
        abstract = True


class PlaceNameLargerScale(PlaceBase):
    """Place name larger scale."""

    class Meta:
        """Meta class for PlaceNameLargerScale."""
        db_table = 'layer"."place_name_larger_scale'
        managed = False


class PlaceNameLargestScale(PlaceBase):
    """Place name largest scale."""

    class Meta:
        """Meta class for PlaceNameLargestScale."""
        db_table = 'layer"."place_name_largest_scale'
        managed = False


class PlaceNameMidScale(PlaceBase):
    """Place name mid scale."""

    class Meta:
        """Meta class for PlaceNameMidScale."""
        db_table = 'layer"."place_name_midscale'
        managed = False


class PlaceNameSmallScale(PlaceBase):
    """Place name small scale."""

    class Meta:
        """Meta class for PlaceNameSmallScale."""
        db_table = 'layer"."place_name_smallest_scale'
        managed = False
