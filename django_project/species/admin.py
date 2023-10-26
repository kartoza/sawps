# -*- coding: utf-8 -*-

from django.contrib import admin, messages
from django.utils.html import format_html
from species.models import TaxonRank, Taxon
from species.forms import TaxonForm


@admin.action(description='Clean output caches')
def clean_output_caches(modeladmin, request, queryset):
    """Clean statistical model output from taxons."""
    from frontend.utils.statistical_model import (
        clear_statistical_model_output_cache
    )
    for taxon in queryset:
        clear_statistical_model_output_cache(taxon)
    modeladmin.message_user(
        request,
        'Statistical model output cache has been cleared!',
        messages.SUCCESS
    )


class TaxonAdmin(admin.ModelAdmin):
    """Admin page for Taxon model

    """
    list_display = ('scientific_name', 'common_name_varbatim',
                    'taxon_rank', 'show_on_front_page', 'display_color')
    search_fields = ['scientific_name', 'common_name_varbatim',
                     'taxon_rank__name']
    form = TaxonForm
    actions = [clean_output_caches]

    def display_color(self, obj):
        return format_html(
            '<span style="width:10px;height:10px;'
            'display:inline-block;background-color:%s"></span>' % obj.colour
        )
    display_color.short_description = 'Colour'
    display_color.allow_tags = True


admin.site.register(TaxonRank)
admin.site.register(Taxon, TaxonAdmin)
