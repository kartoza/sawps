# -*- coding: utf-8 -*-


"""Classes for searching parcels.
"""
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.conf import settings
from property.models import Province
from frontend.models.base_task import BaseTaskRequest

# uploaded file types
GEOJSON = 'GEOJSON'
SHAPEFILE = 'SHAPEFILE'
GEOPACKAGE = 'GEOPACKAGE'
KML = 'KML'


class BoundaryFile(models.Model):
    """Boundary uploaded file."""

    FILE_TYPE_CHOICES = (
        (GEOJSON, GEOJSON),
        (SHAPEFILE, SHAPEFILE),
        (GEOPACKAGE, GEOPACKAGE),
        (KML, KML)
    )

    session = models.CharField(
        blank=False,
        null=False,
        max_length=256
    )

    meta_id = models.CharField(
        blank=True,
        default='',
        max_length=256
    )

    upload_date = models.DateTimeField(
        null=True,
        blank=True
    )

    file = models.FileField(
        upload_to='boundary_files/%Y/%m/%d/'
    )

    file_type = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        choices=FILE_TYPE_CHOICES
    )

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        default='',
        blank=True,
        max_length=512
    )

    def __str__(self):
        return self.name


class BoundarySearchRequest(BaseTaskRequest, gis_models.Model):
    """Boundary search request."""

    type = models.CharField(
        max_length=256,
        help_text='File/Digitise'
    )

    session = models.CharField(
        max_length=256
    )

    request_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    geometry = gis_models.MultiPolygonField(
        srid=4326,
        null=True,
        blank=True
    )

    parcels = models.JSONField(
        default=list,
        null=True,
        blank=True
    )

    used_parcels = models.JSONField(
        default=list,
        null=True,
        blank=True
    )
    property_size_ha = models.FloatField(null=True, blank=True)
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
