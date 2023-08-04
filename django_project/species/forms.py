# -*- coding: utf-8 -*-


"""Species forms.
"""
from django.forms import ModelForm
from django.forms.widgets import TextInput
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
