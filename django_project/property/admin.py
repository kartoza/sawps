# -*- coding: utf-8 -*-


"""Admin for property package.
"""
from django.contrib import admin
from property.models import (
    PropertyType, Province, ParcelType,
    Property,
    Parcel
)


class PropertyAdmin(admin.ModelAdmin):
    """Admin page for Property model.

    """
    list_display = (
        'name',
        'short_code',
        'organisation',
        'property_size_ha',
        'province'
    )
    search_fields = ['name', 'organisation__name', 'province__name']

    @admin.action(
        description="Generate spatial filters for selected properties"
    )
    def generate_spatial_filters_for_properties(self, request, queryset):
        """Admin action to generate spatial filter data for
            selected properties."""
        from property.tasks.generate_spatial_filter import (
            generate_spatial_filter_task
        )
        for property_obj in queryset:
            property_obj.spatialdatamodel_set.all().delete()
            generate_spatial_filter_task.delay(
                property_obj.id
            )

    @admin.action(
        description="Patch centroid field in properties"
    )
    def run_patch_property_centroid(self, request, queryset):
        """Admin action to patch property without centroid."""
        from property.tasks.generate_property_centroid import (
            generate_property_centroid
        )
        generate_property_centroid.delay()

    actions = [generate_spatial_filters_for_properties,
               run_patch_property_centroid]


class ParcelAdmin(admin.ModelAdmin):
    """Admin page for Parcel model.

    """
    list_display = ('sg_number', 'property', 'parcel_type')
    search_fields = ['sg_number', 'property__name', 'parcel_type__name']


class PropertyTypeAdmin(admin.ModelAdmin):
    """Admin page for PropertyType model.

    """
    list_display = ('id', 'name')
    search_fields = ['name']


class ProvinceAdmin(admin.ModelAdmin):
    """Admin page for Province model.

    """
    list_display = ('id', 'name')
    search_fields = ['name']


class ParcelTypeAdmin(admin.ModelAdmin):
    """Admin page for ParcelType model.

    """
    list_display = ('id', 'name')
    search_fields = ['name']


admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(ParcelType, ParcelTypeAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Parcel, ParcelAdmin)
