# -*- coding: utf-8 -*-


"""Admin page for Occurrence models.
"""
from django.contrib import admin
from occurrence.models import SurveyMethod


admin.site.register(SurveyMethod)
