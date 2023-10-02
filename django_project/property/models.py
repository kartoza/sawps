from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class Property(models.Model):
    """Property model."""
    name = models.CharField(max_length=300, unique=True)
    owner_email = models.EmailField(null=True, blank=True)
    property_size_ha = models.IntegerField(null=True, blank=True)
    geometry = models.MultiPolygonField(srid=4326, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING)
    property_type = models.ForeignKey(
        PropertyType, on_delete=models.DO_NOTHING
    )
    organisation = models.ForeignKey(
        'stakeholder.Organisation', on_delete=models.DO_NOTHING
    )

    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField()
    open = models.BooleanField(
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        db_table = 'property'

    def __str__(self):
        return self.name


@receiver(post_save, sender=Property)
def property_post_save(sender, instance: Property,
                       created, *args, **kwargs):
    from property.tasks.generate_spatial_filter import (
        generate_spatial_filter_task
    )
    if created:
        generate_spatial_filter_task.delay(instance.id)


class ParcelType(models.Model):
    """Parcel type model."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Parcel type'
        verbose_name_plural = 'Parcel types'
        db_table = 'parcel_type'


class Parcel(models.Model):
    """Parcel model."""
    sg_number = models.CharField(max_length=100, unique=True)
    year = models.DateField()
    property = models.ForeignKey('property.Property', on_delete=models.CASCADE)
    parcel_type = models.ForeignKey(ParcelType, on_delete=models.CASCADE)
    farm_number = models.IntegerField(
        null=False,
        default=0
    )
    farm_name = models.TextField(
        null=False,
        default=''
    )
    sub_division_number = models.IntegerField(
        null=False,
        default=0
    )

    def __str__(self):
        return self.sg_number

    class Meta:
        verbose_name = 'Parcel'
        verbose_name_plural = 'Parcels'
        db_table = 'parcel'
