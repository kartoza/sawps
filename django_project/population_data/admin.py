# -*- coding: utf-8 -*-


"""Admin for population data package.
"""
from django.contrib import admin
from population_data.models import (
    CountMethod,
    AnnualPopulation,
    AnnualPopulationPerActivity,
    Certainty,
    OpenCloseSystem
)
from population_data.forms import AnnualPopulationForm

class AnnualPopulationAdmin(admin.ModelAdmin):
    form = AnnualPopulationForm

admin.site.register(CountMethod)
admin.site.register(OpenCloseSystem)
admin.site.register(AnnualPopulation, AnnualPopulationAdmin)
admin.site.register(AnnualPopulationPerActivity)
admin.site.register(Certainty)
