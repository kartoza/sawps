from django.contrib import admin
from occurrence.models import (
    SurveyMethod,
    BasisOfRecord,
    SamplingSizeUnit,
    OccurrenceStatus,
)

admin.site.register(SurveyMethod)
admin.site.register(OccurrenceStatus)
admin.site.register(BasisOfRecord)
admin.site.register(SamplingSizeUnit)
