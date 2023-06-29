from django.contrib import admin
from species.models import TaxonRank, Taxon, ManagementStatus, OwnedSpecies

admin.site.register(TaxonRank)
admin.site.register(Taxon)
admin.site.register(ManagementStatus)
admin.site.register(OwnedSpecies)

