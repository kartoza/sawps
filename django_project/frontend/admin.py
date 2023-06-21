from django.contrib import admin
from frontend.models import ContextLayer
from frontend.models import BoundaryFile, BoundarySearchRequest


class BoundaryFileAdmin(admin.ModelAdmin):
    list_display = ('meta_id', 'name', 'upload_date', 'session', 'file_type')


class BoundarySearchRequestAdmin(admin.ModelAdmin):
    list_display = ('session', 'type', 'status', 'progress')


admin.site.register(ContextLayer)
admin.site.register(BoundaryFile, BoundaryFileAdmin)
admin.site.register(BoundarySearchRequest, BoundarySearchRequestAdmin)
