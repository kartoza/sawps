from django.contrib import admin

from occurrence.models import SurveyMethod, BasisOfRecord

admin.site.register(SurveyMethod)

admin.site.register(BasisOfRecord)