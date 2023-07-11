
from django.forms import ModelForm
from django.forms.widgets import TextInput
from species.models import Taxon

class TaxonForm(ModelForm):
    class Meta:
        model = Taxon
        fields = '__all__'
        widgets = {
            'colour': TextInput(attrs={'type': 'color'}),
        }
