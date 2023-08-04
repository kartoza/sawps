# -*- coding: utf-8 -*-


"""Admin page for species models.
"""
from django.contrib import admin
from species.models import TaxonRank, Taxon, OwnedSpecies
from species.forms import TaxonForm


class TaxonAdmin(admin.ModelAdmin):
    """Admin page for Taxon model

    """
    form = TaxonForm


admin.site.register(TaxonRank)
admin.site.register(Taxon, TaxonAdmin)
admin.site.register(OwnedSpecies)
