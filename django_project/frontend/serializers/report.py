from django.db.models import Sum
from rest_framework import serializers

from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity
)
from species.models import OwnedSpecies


class BaseNationalReportSerializer(serializers.Serializer):
    """
    Base Serializer for Report.
    """

    scientific_name = serializers.SerializerMethodField()
    common_name = serializers.SerializerMethodField()

    def get_scientific_name(self, obj: AnnualPopulation) -> str:
        return obj.owned_species.taxon.scientific_name

    def get_common_name(self, obj: AnnualPopulation) -> str:
        return obj.owned_species.taxon.common_name_varbatim


class BaseReportSerializer(serializers.Serializer):
    """
    Base Serializer for Report.
    """

    property_name = serializers.SerializerMethodField()
    scientific_name = serializers.SerializerMethodField()
    common_name = serializers.SerializerMethodField()

    def get_scientific_name(self, obj: AnnualPopulation) -> str:
        return obj.owned_species.taxon.scientific_name

    def get_common_name(self, obj: AnnualPopulation) -> str:
        return obj.owned_species.taxon.common_name_varbatim

    def get_property_name(self, obj: AnnualPopulation) -> str:
        return obj.owned_species.property.name


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
        activity = kwargs.pop('activity', None)
        if not activity:
            raise ValueError("'activity_name' argument is required!")
        super().__init__(*args, **kwargs)

        base_fields = [
            "property_name", "scientific_name", "common_name",
            "year", "total", "adult_male", "adult_female",
            "juvenile_male", "juvenile_female"
        ]
        valid_fields = base_fields + activity.export_fields
        allowed = set(valid_fields)
        existing = set(self.fields.keys())
        for field_name in existing - allowed:
            self.fields.pop(field_name)

    class Meta:
        model = AnnualPopulationPerActivity
        fields = '__all__'


class NationalLevelSpeciesReport(serializers.Serializer):

    def to_representation(self, instance):
        instance['common_name'] = instance['taxon__common_name_varbatim']
        instance['scientific_name'] = instance['taxon__scientific_name']
        del instance['taxon__common_name_varbatim']
        del instance['taxon__scientific_name']
        return instance


class NationalLevelPropertyReport(serializers.Serializer):

    def to_representation(self, instance):
        data = {
            "common_name": (
                instance.common_name_varbatim if
                instance.common_name_varbatim else '-'
            ),
            "scientific_name": instance.scientific_name,
        }

        property_data = OwnedSpecies.objects.values(
            "property__property_type__name",
        ).filter(**self.context['filters'], taxon=instance).annotate(
            population=Sum("annualpopulation__total"),
            area=Sum("property__property_size_ha"),
        )

        for property_entry in property_data:
            property_name = property_entry["property__property_type__name"]
            data[
                f"total_population_{property_name}_property"
            ] = property_entry["population"]
            data[
                f"total_area_{property_name}_property"
            ] = property_entry["area"]

        return data


class NationalLevelActivityReport(serializers.Serializer):

    def to_representation(self, instance):
        data = {
            "common_name": instance.common_name_varbatim,
            "scientific_name": instance.scientific_name,
        }

        activity_data = OwnedSpecies.objects.values(
            "annualpopulationperactivity__activity_type__name",
        ).filter(**self.context['filters'], taxon=instance).annotate(
            population=Sum("annualpopulationperactivity__total"),
        )

        for activity_entry in activity_data:
            activity_name = activity_entry[
                "annualpopulationperactivity__activity_type__name"
            ]
            data[
                f"total_population_{activity_name}"
            ] = activity_entry["population"]

        return data


class NationalLevelProvinceReport(serializers.Serializer):

    def to_representation(self, instance):
        data = {
            "common_name": instance.common_name_varbatim,
            "scientific_name": instance.scientific_name,
        }

        province_data = OwnedSpecies.objects.values(
            "property__province__name",
        ).filter(**self.context['filters'], taxon=instance).annotate(
            population=Sum("annualpopulation__total"),
        )

        for province_entry in province_data:
            province_name = province_entry["property__province__name"]
            data[
                f"total_population_{province_name}"
            ] = province_entry["population"]

        return data
