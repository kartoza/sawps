from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class PropertyType(models.Model):
    name = models.CharField(max_length=250, unique=True)
    colour = models.CharField(
        max_length=20,
        default='#000000'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Property type'
        verbose_name_plural = 'Property types'
        db_table = 'property_type'


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'
        db_table = 'province'


@receiver(pre_save, sender=Province)
def province_pre_save(
    sender, instance: Province, *args, **kwargs
):
    if instance.id:
        old_province = Province.objects.get(id=instance.id)
        if old_province.name != instance.name:
            instance.skip_post_save = False


@receiver(post_save, sender=Province)
def province_post_save(
    sender, instance: Province, created, *args, **kwargs
):
    from property.tasks import update_organisation_property_short_code

    if not created and not getattr(instance, 'skip_post_save', True):
        update_organisation_property_short_code.delay(instance.id)


SELECT_SOURCE_TYPE = 'selection'
DIGITISE_SOURCE_TYPE = 'digitise'
BOUNDARY_FILE_SOURCE_TYPE = 'boundary_file'


class Property(models.Model):
    """Property model."""
    SOURCE_TYPE_CHOICES = (
        (SELECT_SOURCE_TYPE, SELECT_SOURCE_TYPE),
        (DIGITISE_SOURCE_TYPE, DIGITISE_SOURCE_TYPE),
        (BOUNDARY_FILE_SOURCE_TYPE, BOUNDARY_FILE_SOURCE_TYPE)
    )
    name = models.CharField(max_length=300, unique=True)
    short_code = models.CharField(
        max_length=50,
        null=False,
        blank=True
    )
    owner_email = models.EmailField(null=True, blank=True)
    property_size_ha = models.FloatField(null=True, blank=True)
    geometry = models.MultiPolygonField(srid=4326, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    property_type = models.ForeignKey(
        PropertyType, on_delete=models.CASCADE
    )
    organisation = models.ForeignKey(
        'stakeholder.Organisation', on_delete=models.CASCADE
    )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    open = models.ForeignKey(
        "population_data.OpenCloseSystem", on_delete=models.CASCADE, null=True
    )
    centroid = models.PointField(srid=4326, null=True, blank=True)
    boundary_source = models.CharField(
        max_length=255,
        choices=SOURCE_TYPE_CHOICES,
        default=SELECT_SOURCE_TYPE,
        null=True,
        blank=True
    )


    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        db_table = 'property'

    def __str__(self):
        return self.name

    def get_short_code(
        self,
        with_digit: bool = True
    ):
        from property.utils import get_property_short_code

        province_name = self.province.name if self.province else ''
        organisation_name = self.organisation.name if self.organisation else ''
        property_name = self.name
        return get_property_short_code(
            province_name,
            organisation_name,
            property_name,
            with_digit
        )


@receiver(pre_save, sender=Property)
def property_pre_save(
    sender, instance: Property, *args, **kwargs
):
    from property.utils import get_property_short_code

    if instance.id:
        old_property: Property = Property.objects.get(id=instance.id)
        is_name_changed = old_property.name != instance.name
        is_org_changed = old_property.organisation != instance.organisation
        is_province_changed = old_property.province != instance.province
        if any([is_province_changed, is_org_changed, is_name_changed]):
            instance.short_code = get_property_short_code(
                province_name=(
                    instance.province.name if instance.province else ''
                ),
                organisation_name=instance.organisation.name,
                property_name=instance.name,
                with_digit=True
            )
            instance.skip_post_save = False
    else:
        instance.short_code = instance.get_short_code()


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
    sg_number = models.CharField(max_length=100, unique=False)
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
    source = models.CharField(max_length=100, null=True, blank=True)
    source_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.sg_number

    class Meta:
        verbose_name = 'Parcel'
        verbose_name_plural = 'Parcels'
        db_table = 'parcel'


class PropertyOverlaps(models.Model):
    """Model to store property that overlaps with each other."""
    property = models.ForeignKey('property.Property', on_delete=models.CASCADE)
    other = models.ForeignKey('property.Property',
                              on_delete=models.CASCADE, related_name='other')
    reported_at = models.DateTimeField()
    overlap_geom = models.MultiPolygonField(srid=4326, null=True, blank=True)
    overlap_area_size = models.FloatField(null=True, blank=True)
    resolved = models.BooleanField(
        default=False
    )
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Property Overlaps'
        verbose_name_plural = 'Property Overlaps'
