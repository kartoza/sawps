# -*- coding: utf-8 -*-

"""Cadastral Land Parcel tables.

"""
from django.contrib.gis.db import models


class ParcelBase(models.Model):
    """Base Model for Parcel Tables."""

    id = models.AutoField(primary_key=True)

    geom = models.MultiPolygonField(
        null=True,
        srid=3857
    )

    tag_value = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )

    cname = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        db_index=True
    )

    class Meta:
        """Meta class for ParcelBase."""
        abstract = True


class Erf(ParcelBase):
    """Erf Urban Parcel."""

    class Meta:
        """Meta class for Erf."""
        db_table = 'layer"."erf'


class FarmPortion(ParcelBase):
    """Farm Portion Rural Parcel."""

    class Meta:
        """Meta class for FarmPortion."""
        db_table = 'layer"."farm_portion'


class Holding(ParcelBase):
    """Holding Semi Urban Parcel."""

    class Meta:
        """Meta class for Holding."""
        db_table = 'layer"."holding'


class ParentFarm(ParcelBase):
    """ParentFarm Rural Parcel."""

    class Meta:
        """Meta class for ParentFarm."""
        db_table = 'layer"."parent_farm'
