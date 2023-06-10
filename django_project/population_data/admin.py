from django.contrib import admin
from population_data.models import CountMethod, Month, NatureOfPopulation, PopulationCount, PopulationCountPerActivity

admin.site.register(CountMethod)
admin.site.register(Month)
admin.site.register(NatureOfPopulation)
admin.site.register(PopulationCount)
admin.site.register(PopulationCountPerActivity)


