from django.forms import ModelForm
from population_data.models import AnnualPopulation


class AnnualPopulationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.fields['certainty'].label = 'Population estimate certainty'


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
            "certainty",
            "open_close_system",
            "presence",
            "population_status",
            "population_estimate_category",
            "sampling_effort_coverage",
            "upper_confidence_level",
            "lower_confidence_level",
            "certainty_of_bounds",
            "population_estimate_certainty",
            "note",
        )
