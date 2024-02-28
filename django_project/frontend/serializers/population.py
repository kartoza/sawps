"""Serializer for population classess."""
from rest_framework import serializers
from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity
)


class ActivityFormSerializer(serializers.ModelSerializer):
    """AnnualPopulationPerActivity serializer."""

    activity_type_name = serializers.SerializerMethodField()
    permit = serializers.SerializerMethodField()

    def get_activity_type_name(self, obj: AnnualPopulationPerActivity):
        return obj.activity_type.name

    def get_permit(self, obj: AnnualPopulationPerActivity):
        if obj.activity_type.recruitment:
            return obj.intake_permit
        return obj.offtake_permit

    class Meta:
        model = AnnualPopulationPerActivity
        fields = [
            'activity_type_id', 'activity_type_name', 'total',
            'adult_male', 'adult_female', 'juvenile_male', 'juvenile_female',
            'founder_population', 'reintroduction_source', 'permit',
            'translocation_destination', 'note', 'id'
        ]


class AnnualPopulationFormSerializer(serializers.ModelSerializer):
    """Annual Population data serializer."""

    present = serializers.SerializerMethodField()
    survey_method_name = serializers.SerializerMethodField()
    sampling_effort_coverage_name = serializers.SerializerMethodField()
    population_status_name = serializers.SerializerMethodField()
    population_estimate_category_name = serializers.SerializerMethodField()

    def get_present(self, obj: AnnualPopulation):
        return obj.presence

    def get_survey_method_name(self, obj: AnnualPopulation):
        return obj.survey_method.name if obj.survey_method else ''

    def get_sampling_effort_coverage_name(self, obj: AnnualPopulation):
        return (
            obj.sampling_effort_coverage.name if
            obj.sampling_effort_coverage else ''
        )

    def get_population_status_name(self, obj: AnnualPopulation):
        return obj.population_status.name if obj.population_status else ''

    def get_population_estimate_category_name(self, obj: AnnualPopulation):
        return (
            obj.population_estimate_category.name if
            obj.population_estimate_category else ''
        )

    class Meta:
        model = AnnualPopulation
        fields = [
            'present', 'total', 'adult_total', 'adult_male', 'adult_female',
            'sub_adult_total', 'sub_adult_male', 'sub_adult_female',
            'juvenile_total', 'juvenile_male', 'juvenile_female', 'group',
            'area_available_to_species', 'survey_method_id',
            'survey_method_name', 'note', 'population_estimate_certainty',
            'upper_confidence_level', 'lower_confidence_level',
            'certainty_of_bounds', 'sampling_effort_coverage_id',
            'sampling_effort_coverage_name', 'population_status_id',
            'population_status_name', 'population_estimate_category_id',
            'population_estimate_category_name',
            'population_estimate_category_other',
            'survey_method_other'
        ]
