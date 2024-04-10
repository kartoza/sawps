# -*- coding: utf-8 -*-


"""Admin for property package.
"""
from django.contrib import admin, messages
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html
from property.models import (
    PropertyType, Province, ParcelType,
    Property,
    Parcel,
    PropertyOverlaps
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

    @admin.action(
        description="Run check overlaps"
    )
    def run_check_overlaps(modeladmin, request, queryset):
        """Admin action to check for overlapping properties."""
        from property.tasks.check_overlaps import (
            property_check_overlaps_each_other
        )
        property_check_overlaps_each_other.delay()
        modeladmin.message_user(
            request,
            'Job check for overlapping properties will be run in background!',
            messages.SUCCESS
        )

    actions = [generate_spatial_filters_for_properties,
               run_patch_property_centroid, run_patch_property_province,
               run_check_overlaps]


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

    actions = [run_patch_parcel_source]


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


class PropertyOverlapsAdmin(admin.ModelAdmin):
    """Admin page for PropertyOverlaps model.

    """
    list_display = ('property', 'get_property_owner',
                    'get_other_property', 'get_other_property_owner',
                    'reported_at', 'get_overlap_size', 'resolved')
    search_fields = ['property__name', 'other__name']

    def format_user_cell(self, user):
        url = reverse(
            f'admin:{user._meta.app_label}_{user._meta.model_name}_change',
            args=[user.id]
        )
        return format_html(
            '<a href="%s">%s</a>' % (url, user.get_full_name())
        )

    @admin.display(ordering='property__created_by__first_name',
                   description='Property Owner')
    def get_property_owner(self, obj):
        return self.format_user_cell(obj.property.created_by)

    @admin.display(ordering='other__name',
                   description='Other Property')
    def get_other_property(self, obj):
        return obj.other.name

    @admin.display(ordering='other__created_by__first_name',
                   description='Other Property Owner')
    def get_other_property_owner(self, obj):
        return self.format_user_cell(obj.other.created_by)

    @admin.display(ordering='overlap_area_size',
                   description='Overlap area size')
    def get_overlap_size(self, obj):
        if obj.overlap_area_size < 10000:
            return f'{obj.overlap_area_size:.2f} sqm'
        return f'{obj.overlap_area_size / 10000:.2f} ha'

    @admin.action(
        description="Resolve overlaps record"
    )
    def resolve_overlaps(modeladmin, request, queryset):
        """Admin action to manually resolve the overlap record."""
        for overlap in queryset:
            overlap.resolved = True
            overlap.resolved_at = timezone.now()
            overlap.save(update_fields=['resolved', 'resolved_at'])
        modeladmin.message_user(
            request,
            (
                f'{queryset.count()} records has successfully been '
                'marked as resolved!'
            ),
            messages.SUCCESS
        )
    actions = [resolve_overlaps]


admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(ParcelType, ParcelTypeAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Parcel, ParcelAdmin)
admin.site.register(PropertyOverlaps, PropertyOverlapsAdmin)
