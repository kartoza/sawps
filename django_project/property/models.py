from django.contrib.gis.db import models


class Province(models.Model):
    """province model"""

    name = models.CharField(unique=True, max_length=150)

    class Meta:
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'


class PropertyType(models.Model):
    """property type model"""

    property_types = (
        ('community', 'Community'),
        ('provincial', 'Provincial'),
        ('national', 'National'),
        ('state', 'State'),
        ('private', 'Private'),
        ('state and private', 'State and Private'),
    )
    name = models.CharField(
        max_length=200, choices=property_types, unique=True
    )

    class Meta:
        verbose_name = 'Property type'
        verbose_name_plural = 'Property types'


class OwnershipStatus(models.Model):
    """ownership status model"""

    status = [('owner', 'Owner')]
    name = models.CharField(max_length=100, choices=status)


class Property(models.Model):
    """property model"""

    name = models.CharField(max_length=300, unique=True)
    owner_email = models.EmailField(null=True, blank=True)
    property_size_ha = models.IntegerField(null=True, blank=True)
    area_available = models.FloatField()
    geometry = models.PolygonField(srid=4326, null=True, blank=True)
    province_id = models.ForeignKey(Province, on_delete=models.DO_NOTHING)
    ownership_status_id = models.ForeignKey(
        OwnershipStatus, on_delete=models.DO_NOTHING
    )
    property_type_id = models.ForeignKey(
        PropertyType, on_delete=models.DO_NOTHING
    )
    organization_id = models.ForeignKey(
        'stakeholder.Organization', on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    area_available__lte=models.F('property_size_ha')
                ),
                name='check property size',
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
