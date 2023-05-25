from django.contrib import admin
from . import models

admin.site.register(models.VectorLayer)
admin.site.register(models.RasterLayer)
admin.site.register(models.WMS)
admin.site.register(models.Feature)