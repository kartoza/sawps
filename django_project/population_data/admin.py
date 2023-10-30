"""Admin for population data package.
"""
from django.contrib import admin
from population_data.forms import AnnualPopulationForm
from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity,
    OpenCloseSystem,
    SamplingEffortCoverage,
    PopulationStatus,
    PopulationEstimateCategory
)


class AnnualPopulationAdmin(admin.ModelAdmin):
    """Admin page for AnnualPopulation model

    """
    list_display = (
        'owned_species',
        'year',
        'total',
        'adult_male',
        'adult_female',
        'juvenile_male',
        'juvenile_female',
        'sub_adult_total',
        'sub_adult_male',
        'sub_adult_female',
        'juvenile_total',
        'survey_method',
        'sampling_size_unit',
        'certainty',
        'open_close_system',
        'group'
    )
    search_fields = [
        'year',
        'owned_species__property__name',
        'total',
        'adult_male',
        'adult_female',
        'juvenile_male',
        'juvenile_female',
        'sub_adult_total',
        'sub_adult_male',
        'sub_adult_female',
        'juvenile_total'
    ]
    form = AnnualPopulationForm


class OpenCloseSystemAdmin(admin.ModelAdmin):
    """Admin page for OpenCloseSystem model

    """
    list_display = ('id', 'name',)
    search_fields = ['name']


admin.site.register(OpenCloseSystem, OpenCloseSystemAdmin)
admin.site.register(AnnualPopulation, AnnualPopulationAdmin)


@admin.register(AnnualPopulationPerActivity)
class AnnualPopulationPerActivityAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'property_name',
        'year',
        'activity_type',
        'total'
    ]
    # list_filter = [
    #     'owned_species__property',
    #     'year',
    #     'activity_type'
    # ]
    search_fields = [
        'owned_species__property__name',
        'owned_species__taxon__scientific_name',
        'owned_species__taxon__common_name_varbatim'
    ]

    def property_name(self, obj: AnnualPopulationPerActivity):
        return obj.owned_species.property.name


class SamplingEffortCoverageAdmin(admin.ModelAdmin):
    """Admin page for SamplingEffortCoverage model

    """
    list_display = ('id', 'name', 'sort_order')
    search_fields = ['name', 'sort_order']


class PopulationStatusAdmin(admin.ModelAdmin):
    """Admin page for PopulationStatus model

    """
    list_display = ('id', 'name')
    search_fields = ['name']


class PopulationEstimateCategoryAdmin(admin.ModelAdmin):
    """Admin page for PopulationEstimateCategory model

    """
    list_display = ('id', 'name')
    search_fields = ['name']


admin.site.register(SamplingEffortCoverage, SamplingEffortCoverageAdmin)
admin.site.register(PopulationStatus, PopulationStatusAdmin)
admin.site.register(
    PopulationEstimateCategory,
    PopulationEstimateCategoryAdmin
)
