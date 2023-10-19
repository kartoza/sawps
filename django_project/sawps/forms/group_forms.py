from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelMultipleChoiceField, ModelForm
from sawps.models import ExtendedGroup, ExtendedGroupPermission


class ExtendedGroupForm(ModelForm):
    permissions = ModelMultipleChoiceField(
        queryset=ExtendedGroupPermission.objects.all(),
        widget=FilteredSelectMultiple("verbose name", is_stacked=False)
    )

    class Meta:
        model = ExtendedGroup
        fields = '__all__'