"""Admin for population data package.
"""
from django.contrib import admin
from population_data.forms import AnnualPopulationForm
from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity,
    Certainty,
    CountMethod,
    OpenCloseSystem,
    SamplingEffortCoverage,
    PopulationStatus,
    PopulationEstimateCategory
)


class AnnualPopulationAdmin(admin.ModelAdmin):
    form = AnnualPopulationForm


admin.site.register(CountMethod)
admin.site.register(OpenCloseSystem)
admin.site.register(AnnualPopulation, AnnualPopulationAdmin)
admin.site.register(AnnualPopulationPerActivity)
admin.site.register(Certainty)
admin.site.register(SamplingEffortCoverage)
admin.site.register(PopulationStatus)
admin.site.register(PopulationEstimateCategory)
