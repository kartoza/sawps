from django.contrib import admin

from species.models import TaxonRank, Taxon, ManagementStatus

admin.site.register(TaxonRank)
admin.site.register(Taxon)
admin.site.register(ManagementStatus)
