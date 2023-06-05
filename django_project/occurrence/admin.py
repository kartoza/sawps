from django.contrib import admin

from occurrence.models import SurveyMethod, OccurrenceStatus

admin.site.register(SurveyMethod)
admin.site.register(OccurrenceStatus)