from rest_framework import serializers

from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity
)
from species.models import OwnedSpecies


class BaseReportSerializer(serializers.Serializer):
    """
    Base Serializer for Report.
    """

    property_name = serializers.SerializerMethodField()
    scientific_name = serializers.SerializerMethodField()
    common_name = serializers.SerializerMethodField()

    def get_property_name(self, obj: AnnualPopulation) -> str:
        return obj.owned_species.property.name

    def get_scientific_name(self, obj: AnnualPopulation) -> str:
        return obj.owned_species.taxon.scientific_name

    def get_common_name(self, obj: AnnualPopulation) -> str:
        return obj.owned_species.taxon.common_name_varbatim


class SpeciesReportSerializer(
    serializers.ModelSerializer,
    BaseReportSerializer
):
    """
    Serializer for Species Report.
    """

    class Meta:
        model = AnnualPopulation
        fields = [
            "property_name", "scientific_name", "common_name",
            "year", "group", "total", "adult_male", "adult_female",
            "juvenile_male", "juvenile_female", "sub_adult_male",
            "sub_adult_female",
        ]


class SamplingReportSerializer(
    serializers.ModelSerializer,
    BaseReportSerializer
):
    """
    Serializer for Sampling Report.
    """

    population_status = serializers.SerializerMethodField()
    population_estimate_category = serializers.SerializerMethodField()
    survey_method = serializers.SerializerMethodField()
    sampling_effort_coverage = serializers.SerializerMethodField()

    def get_population_status(self, obj: AnnualPopulation) -> str:
        return obj.population_status.name if \
            obj.population_status else ""

    def get_population_estimate_category(self, obj: AnnualPopulation) -> str:
        return obj.population_estimate_category.name if \
            obj.population_estimate_category else ""

    def get_survey_method(self, obj: AnnualPopulation) -> str:
        return obj.survey_method.name if \
            obj.survey_method else ""

    def get_sampling_effort_coverage(self, obj: AnnualPopulation) -> str:
        return obj.sampling_effort_coverage.name if \
            obj.sampling_effort_coverage else ""

    class Meta:
        model = AnnualPopulation
        fields = [
            "property_name",
            "scientific_name",
            "common_name",
            "population_status",
            "population_estimate_category",
            "survey_method",
            "sampling_effort_coverage",
            "population_estimate_certainty",
        ]


class PropertyReportSerializer(
    serializers.ModelSerializer,
    BaseReportSerializer
):
    """
    Serializer for Property Report.
    """

    property_name = serializers.SerializerMethodField()
    scientific_name = serializers.SerializerMethodField()
    common_name = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    owner_email = serializers.SerializerMethodField()
    property_type = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()
    property_size_ha = serializers.SerializerMethodField()
    open_close_systems = serializers.SerializerMethodField()

    def get_property_name(self, obj: OwnedSpecies) -> str:
        return obj.property.name

    def get_scientific_name(self, obj: OwnedSpecies) -> str:
        return obj.taxon.scientific_name

    def get_common_name(self, obj: OwnedSpecies) -> str:
        return obj.taxon.common_name_varbatim

    def get_owner(self, obj: OwnedSpecies) -> str:
        return obj.property.created_by.first_name

    def get_owner_email(self, obj: OwnedSpecies) -> str:
        return obj.property.owner_email

    def get_property_type(self, obj: OwnedSpecies) -> str:
        return obj.property.property_type.name

    def get_province(self, obj: OwnedSpecies) -> str:
        return obj.property.province.name

    def get_property_size_ha(self, obj: OwnedSpecies) -> str:
        return obj.property.property_size_ha

    def get_open_close_systems(self, obj: OwnedSpecies) -> str:
        return obj.property.open.name if obj.property.open else ""

    class Meta:
        model = OwnedSpecies
        fields = [
            "property_name",
            "scientific_name",
            "common_name",
            "owner",
            "owner_email",
            "property_type",
            "province",
            "property_size_ha",
            "area_available_to_species",
            "open_close_systems"
        ]


class ActivityReportSerializer(
    serializers.ModelSerializer,
    BaseReportSerializer
):
    """
    Serializer for Activity Report.
    The serializer uses dynamic column based on the
    selected activity.
    """

    def __init__(self, *args, **kwargs):
        activity_name = kwargs.pop('activity_name', None)
        if not activity_name:
            raise ValueError("'activity_name' argument is required!")
        super().__init__(*args, **kwargs)

        activity_data_map = {
            "Unplanned/illegal hunting": [],
            "Planned euthanasia": ["intake_permit"],
            "Planned hunt/cull": ["intake_permit"],
            "Planned translocation": [
                "intake_permit", "translocation_destination",
                "offtake_permit"
            ],
            "Unplanned/natural deaths": [
                "translocation_destination", "founder_population",
                "reintroduction_source"
            ],
        }
        base_fields = [
            "property_name", "scientific_name", "common_name",
            "year", "total", "adult_male", "adult_female",
            "juvenile_male", "juvenile_female"
        ]
        valid_fields = base_fields + activity_data_map[activity_name]
        allowed = set(valid_fields)
        existing = set(self.fields.keys())
        for field_name in existing - allowed:
            self.fields.pop(field_name)

    class Meta:
        model = AnnualPopulationPerActivity
        fields = '__all__'
