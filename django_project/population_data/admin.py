# -*- coding: utf-8 -*-


"""Admin for population data package.
"""
from django.contrib import admin
from population_data.models import (
    CountMethod,
    Month,
    NatureOfPopulation,
    AnnualPopulation,
    AnnualPopulationPerActivity,
    Certainty,
    OpenCloseSystem
)

admin.site.register(CountMethod)
admin.site.register(Month)
admin.site.register(OpenCloseSystem)
admin.site.register(NatureOfPopulation)
admin.site.register(AnnualPopulation)
admin.site.register(AnnualPopulationPerActivity)
admin.site.register(Certainty)
