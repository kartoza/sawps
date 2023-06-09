from django.contrib import admin
from property.models import PropertyType, Province, OwnershipStatus


admin.site.register(PropertyType)
admin.site.register(Province)
admin.site.register(OwnershipStatus)