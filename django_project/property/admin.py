from django.contrib import admin
from property.models import (
    PropertyType, Province, ParcelType,
    Property,
    Parcel, OwnershipStatus
)


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'organisation', 'property_size_ha', 'province')
    search_fields = ['name', 'organisation__name', 'province__name']


class ParcelAdmin(admin.ModelAdmin):
    list_display = ('sg_number', 'property', 'parcel_type')
    search_fields = ['sg_number', 'property__name', 'parcel_type__name']


admin.site.register(PropertyType)
admin.site.register(Province)
admin.site.register(ParcelType)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Parcel, ParcelAdmin)
admin.site.register(OwnershipStatus)
