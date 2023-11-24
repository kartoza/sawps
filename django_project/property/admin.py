# -*- coding: utf-8 -*-


"""Admin for property package.
"""
from django.contrib import admin
from django.utils.html import format_html
from property.models import (
    PropertyType, Province, ParcelType,
    Property,
    Parcel
)
from property.forms import PropertyTypeForm


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
    list_filter = ['province', 'property_type', 'open']
    autocomplete_fields = [
        'province', 'property_type', 'open', 'created_by', 'organisation'
    ]

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

    @admin.action(
        description="Patch province in properties"
    )
    def run_patch_property_province(self, request, queryset):
        """Admin action to patch province in properties."""
        from frontend.tasks.patch_province import (
            patch_province_in_properties
        )
        patch_province_in_properties.delay()

    actions = [generate_spatial_filters_for_properties,
               run_patch_property_centroid, run_patch_property_province]


class ParcelAdmin(admin.ModelAdmin):
    """Admin page for Parcel model.

    """
    list_display = ('sg_number', 'property', 'parcel_type', 'source')
    search_fields = ['sg_number', 'property__name', 'parcel_type__name',
                     'source']
    list_filter = ('parcel_type', 'source')

    @admin.action(
        description="Patch source in parcels"
    )
    def run_patch_parcel_source(self, request, queryset):
        """Admin action to patch source in parcels."""
        from frontend.tasks.parcel import (
            patch_parcel_sources
        )
        patch_parcel_sources.delay()

    actions = [run_patch_parcel_source,]


class PropertyTypeAdmin(admin.ModelAdmin):
    """Admin page for PropertyType model.

    """
    form = PropertyTypeForm
    list_display = ('id', 'name', 'display_color')
    search_fields = ['name']

    def display_color(self, obj):
        return format_html(
            '<span style="width:10px;height:10px;'
            'display:inline-block;background-color:%s"></span>' % obj.colour
        )
    display_color.short_description = 'Colour'
    display_color.allow_tags = True


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
