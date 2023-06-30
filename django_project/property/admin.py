from django.contrib import admin
from property.models import (
    PropertyType, 
    Province, 
    ParcelType, 
    Parcel, 
    Property
)

admin.site.register(PropertyType)
admin.site.register(Province)
admin.site.register(ParcelType)
admin.site.register(Parcel)
admin.site.register(Property)

