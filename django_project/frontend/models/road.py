# -*- coding: utf-8 -*-

"""Road table from layer schema.

"""
from django.contrib.gis.db import models


class Road(models.Model):
    """Model for Road Tables."""

    id = models.AutoField(primary_key=True)

    geom = models.MultiPolygonField(
        null=True,
        srid=3857
    )

    name = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        db_index=True
    )

    highway = models.CharField(
        max_length=80,
        blank=True,
        null=True
    )

    class Meta:
        """Meta class for Road."""
        db_table = 'layer"."zaf_roads'
        managed = False
