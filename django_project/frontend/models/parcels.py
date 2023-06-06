"""Cadastral Land Parcel tables."""
from django.contrib.gis.db import models


class Erf(models.Model):
    """Erf Urban Parcel."""

    fid = models.AutoField(primary_key=True)

    geom = models.GeometryField(
        null=True,
        srid=3857
    )

    tag_value = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )

    id = models.CharField(
        max_length=60,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta class for Erf."""
        db_table = 'layer"."erf'


class FarmPortion(models.Model):
    """Farm Portion Rural Parcel."""

    fid = models.AutoField(primary_key=True)

    geom = models.GeometryField(
        null=True,
        srid=3857
    )

    tag_value = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )

    id = models.CharField(
        max_length=60,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta class for FarmPortion."""
        db_table = 'layer"."farm_portion'


class Holding(models.Model):
    """Holding Semi Urban Parcel."""

    fid = models.AutoField(primary_key=True)

    geom = models.GeometryField(
        null=True,
        srid=3857
    )

    tag_value = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )

    id = models.CharField(
        max_length=60,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta class for Holding."""
        db_table = 'layer"."holding'


class ParentFarm(models.Model):
    """ParentFarm Rural Parcel."""

    fid = models.AutoField(primary_key=True)

    geom = models.GeometryField(
        null=True,
        srid=3857
    )

    tag_value = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )

    id = models.CharField(
        max_length=60,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta class for ParentFarm."""
        db_table = 'layer"."parent_farm'
