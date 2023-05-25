from django.contrib.gis.db import models


class AbstractLayer(models.Model):
    """
    Abstract base class for different layer types
    """
    name = models.CharField(max_length=512)
    type = models.CharField(max_length=15)
    extent = models.CharField(null=True, max_length=20)
    srid = models.CharField(null=True, default='4326', max_length=4)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class VectorLayer(AbstractLayer):
    """
    vector layer, no need to add more fields 
    """
    class Meta:
        verbose_name = "Vector layer"
        verbose_name_plural = "Vector layers"

class WMS(AbstractLayer):
    """
    WMS, get the url only and ingest it directly on
    mapping lib
    """
    url = models.URLField()

    class Meta:
        verbose_name = "WMS"
        verbose_name_plural = "WMS"



class RasterLayer(AbstractLayer):
    """
    raster layer, geoDjango has a RasterField field 
    to handle rasters instead of usual ImageField
    """
    raster_file = models.RasterField()

    class Meta:
        verbose_name = "Raster layer"
        verbose_name_plural = "Raster layers"


class Feature(models.Model):
    """Feature for vector layers defined by it's geom field,
      we are using Geometry base class to handle all geom types"""
    layer_id = models.ForeignKey(VectorLayer, on_delete=models.CASCADE, related_name="features")
    geom= models.GeometryField()
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Feature"
        verbose_name_plural = "Features"
