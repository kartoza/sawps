from django.forms import ModelForm, TextInput
from property.models import PropertyType


class PropertyTypeForm(ModelForm):
    """
    Property Type form.
    """
    class Meta:
        model = PropertyType
        fields = '__all__'
        widgets = {
            'colour': TextInput(attrs={'type': 'color'}),
        }
