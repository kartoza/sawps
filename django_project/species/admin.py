from django.contrib import admin

from species.models import TaxonRank, Taxon

admin.site.register(TaxonRank)
admin.site.register(Taxon)