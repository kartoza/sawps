from django.db import models


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
    #property = models.ForeignKey('property.Property', on_delete=models.DO_NOTHING)
    parcel_type = models.ForeignKey(ParcelType, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.sg_number
    
    class Meta:
        verbose_name = 'Parcel'
        verbose_name_plural = 'Parcels'
        db_table = 'parcel'
