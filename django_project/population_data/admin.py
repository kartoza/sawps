"""Admin for population data package.
"""
from django.contrib import admin
from population_data.forms import AnnualPopulationForm
from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity,
    OpenCloseSystem,
    PopulationEstimateCategory,
    PopulationStatus,
    SamplingEffortCoverage,
)


class AnnualPopulationAdmin(admin.ModelAdmin):
    form = AnnualPopulationForm


admin.site.register(OpenCloseSystem)
admin.site.register(AnnualPopulation, AnnualPopulationAdmin)


@admin.register(AnnualPopulationPerActivity)
class AnnualPopulationPerActivityAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'property_name',
        'scientific_name',
        'common_name',
        'year',
        'activity_type',
        'total'
    ]
    search_fields = [
        'owned_species__property__name',
        'owned_species__taxon__scientific_name',
        'owned_species__taxon__common_name_varbatim'
    ]

    def property_name(self, obj: AnnualPopulationPerActivity):
        return obj.owned_species.property.name

    def scientific_name(self, obj: AnnualPopulationPerActivity):
        return obj.owned_species.taxon.scientific_name

    def common_name(self, obj: AnnualPopulationPerActivity):
        return obj.owned_species.taxon.common_name_varbatim


admin.site.register(SamplingEffortCoverage)
admin.site.register(PopulationStatus)
admin.site.register(PopulationEstimateCategory)
