from django.contrib.gis.db import models
from django.contrib.auth.models import User

class PropertyType(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Property type'
        verbose_name_plural = 'Property types'
        db_table = 'property_type'


class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'
        db_table = 'province'

class OwnershipStatus(models.Model):
    """Ownership status model."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "ownership status"
        verbose_name_plural = "ownership status"
        db_table = "ownership_status"


class Property(models.Model):
    """Property model."""
    name = models.CharField(max_length=300, unique=True)
    owner_email = models.EmailField(null=True, blank=True)
    property_size_ha = models.IntegerField(null=True, blank=True)
    area_available = models.FloatField()
    geometry = models.GeometryField(srid=4326, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING)
    ownership_status = models.ForeignKey(
        OwnershipStatus, on_delete=models.DO_NOTHING
    )
    property_type = models.ForeignKey(
        PropertyType, on_delete=models.DO_NOTHING
    )
    organization = models.ForeignKey(
        'stakeholder.Organization', on_delete=models.DO_NOTHING
    )

    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField()

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        db_table = 'property'
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    area_available__lte=models.F('property_size_ha')
                ),
                name='check property size',
            ),
        ]