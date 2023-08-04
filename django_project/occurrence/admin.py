# -*- coding: utf-8 -*-


"""Admin page for Occurrence models.
"""
from django.contrib import admin
from occurrence.models import (
    SurveyMethod,
    SamplingSizeUnit,
)

admin.site.register(SurveyMethod)
admin.site.register(SamplingSizeUnit)
