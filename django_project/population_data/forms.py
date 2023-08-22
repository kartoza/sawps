from django.forms import ModelForm
from population_data.models import AnnualPopulation


class AnnualPopulationForm(ModelForm):
    class Meta:
        model = AnnualPopulation
        fields = (
            "year",
            "owned_species",
            "total",
            "adult_male",
            "adult_female",
            "sub_adult_total",
            "sub_adult_male",
            "sub_adult_female",
            "juvenile_total",
            "group",
            "juvenile_male",
            "juvenile_female",
            "survey_method",
            "count_method",
            "sampling_size_unit",
            "certainty",
            "open_close_system",
            "presence",
            "note",
        )
