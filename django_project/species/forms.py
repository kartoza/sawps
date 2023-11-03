# -*- coding: utf-8 -*-


"""Species forms.
"""
from django.forms import ModelForm
from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe
from species.models import Taxon


class TaxonForm(ModelForm):
    """Taxon form.

    """
    class Meta:
        model = Taxon
        fields = '__all__'
        widgets = {
            'colour': TextInput(attrs={'type': 'color'}),
        }
        help_texts = {
            'graph_icon': mark_safe(
                "Use SVG file with black fill and transparent background. "
                "It will be used as species icon in graph/charts. <a href='%s' target='_blank'>Click here for sample!</a>" % (
                '/static/images/lion-black.svg')
            ),
            'icon': mark_safe(
                "Will be used at home to display population overview. "
                "<a href='%s' target='_blank'>Click here for sample!</a>" % (
                    '/static/images/leo.png')
            )
        }
