from django.contrib.gis.db import models


class Province(models.Model):
    """province model"""

    name = models.CharField(unique=True)

    class Meta:
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'


class PropertyType(models.Model):
    """property type model"""

    property_types = (
        'Community',
        'Provincial',
        'National',
        'State',
        'Private',
        'State and Private',
    )
    name = models.CharField(
        max_length=200, choices=property_types, unique=True
    )

    class Meta:
        verbose_name = 'Property type'
        verbose_name_plural = 'Property types'


class Property(models.Model):
    """property model"""

    name = models.CharField(max_length=300, unique=True)
    owner_email = models.EmailField(null=True, blank=True)
    property_size_ha = models.IntegerField(null=True, blank=True)
    area_available = models.FloatField()
    geometry = models.PolygonField(srid=4326)
    province_id = models.ForeignKey(Province, on_delete=models.DO_NOTHING)
    ownership_status_id = models.ForeignKey(on_delete=models.DO_NOTHING)
    property_type_id = models.ForeignKey(
        PropertyType, on_delete=models.DO_NOTHING
    )
    organization_id = models.ForeignKey(on_delete=models.DO_NOTHING)
    threshold = 0

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    area_available__gte=models.F('property_size_ha')
                ),
                name='check property size',
            ),
            models.CheckConstraint(
                check=models.Q(area_available_ha__gt=models.F('threshold')),
                name='check threshold area',
            ),
        ]


class Parcel(models.Model):
    """parcel model"""

    sg_number = models.IntegerField(unique=True)
    year = models.DateField()
    property_id = models.ForeignKey(Property, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Parcel'
        verbose_name_plural = 'Parcels'
