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


class WMS(AbstractLayer):
    """
    WMS, get the url only and ingest it directly on
    mapping lib
    """

    url = models.URLField()

    class Meta:
        verbose_name = 'WMS'
        verbose_name_plural = 'WMS'
