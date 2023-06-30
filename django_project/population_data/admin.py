from django.contrib import admin
from population_data.models import (
    CountMethod, 
    Month, 
    NatureOfPopulation, 
    AnnualPopulation, 
    AnnualPopulationPerActivity
)

admin.site.register(CountMethod)
admin.site.register(Month)
admin.site.register(NatureOfPopulation)
admin.site.register(AnnualPopulation)
admin.site.register(AnnualPopulationPerActivity)


