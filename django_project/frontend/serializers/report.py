from django.db.models import Sum
from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity
)
from rest_framework import serializers


class BaseReportSerializer(serializers.Serializer):
    """
    Base Serializer for Report.
    """

    property_name = serializers.SerializerMethodField()
    property_short_code = serializers.SerializerMethodField()
    organisation_name = serializers.SerializerMethodField()
    organisation_short_code = serializers.SerializerMethodField()
    scientific_name = serializers.SerializerMethodField()
    common_name = serializers.SerializerMethodField()

    def get_scientific_name(self, obj: AnnualPopulation) -> str:
        return obj.taxon.scientific_name

    def get_common_name(self, obj: AnnualPopulation) -> str:
        return obj.taxon.common_name_verbatim

    def get_property_name(self, obj: AnnualPopulation) -> str:
        return obj.property.name

    def get_property_short_code(self, obj: AnnualPopulation) -> str:
        return obj.property.short_code

    def get_organisation_name(self, obj: AnnualPopulation) -> str:
        return obj.property.organisation.name

    def get_organisation_short_code(self, obj: AnnualPopulation) -> str:
        return obj.property.organisation.short_code


class BaseSpeciesReportSerializer(
    serializers.ModelSerializer,
    BaseReportSerializer
):
    """
    Serializer for Species Report (for exporting to csv/excel).
    """

    class Meta:
        model = AnnualPopulation
        fields = [
            "property_name", "property_short_code",
            "organisation_name", "organisation_short_code",
            "scientific_name", "common_name",
            "year", "group", "total", "adult_male", "adult_female",
            "juvenile_male", "juvenile_female", "sub_adult_male",
            "sub_adult_female"
        ]


class SpeciesReportSerializer(BaseSpeciesReportSerializer):
    """
    Serializer for Species Report.
    """
    upload_id = serializers.SerializerMethodField()
    is_editable = serializers.SerializerMethodField()

    def get_upload_id(self, obj: AnnualPopulation):
        return obj.id

    def get_is_editable(self, obj: AnnualPopulation):
        user = self.context.get('user', None)
        managed_organisations = self.context.get('managed_ids', [])
        return obj.is_editable(user, managed_organisations)

    class Meta:
        model = AnnualPopulation
        fields = [
            "property_name", "property_short_code",
            "organisation_name", "organisation_short_code",
            "scientific_name", "common_name",
            "year", "group", "total", "adult_male", "adult_female",
            "juvenile_male", "juvenile_female", "sub_adult_male",
            "sub_adult_female", "upload_id", "property_id",
            "is_editable"
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
            "property_short_code",
            "organisation_name",
            "organisation_short_code",
            "year",
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
    property_short_code = serializers.SerializerMethodField()
    organisation_name = serializers.SerializerMethodField()
    organisation_short_code = serializers.SerializerMethodField()
    scientific_name = serializers.SerializerMethodField()
    common_name = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    owner_email = serializers.SerializerMethodField()
    property_type = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()
    property_size_ha = serializers.SerializerMethodField()
    open_close_systems = serializers.SerializerMethodField()
    area_available_to_species = serializers.SerializerMethodField()

    def get_property_name(self, obj: AnnualPopulation) -> str:
        return obj.property.name

    def get_property_short_code(self, obj: AnnualPopulation) -> str:
        return obj.property.short_code

    def get_organisation_name(self, obj: AnnualPopulation) -> str:
        return obj.property.organisation.name

    def get_organisation_short_code(self, obj: AnnualPopulation) -> str:
        return obj.property.organisation.short_code

    def get_scientific_name(self, obj: AnnualPopulation) -> str:
        return obj.taxon.scientific_name

    def get_common_name(self, obj: AnnualPopulation) -> str:
        return obj.taxon.common_name_verbatim

    def get_owner(self, obj: AnnualPopulation) -> str:
        return obj.property.created_by.first_name

    def get_owner_email(self, obj: AnnualPopulation) -> str:
        return obj.property.owner_email

    def get_property_type(self, obj: AnnualPopulation) -> str:
        return obj.property.property_type.name

    def get_province(self, obj: AnnualPopulation) -> str:
        return obj.property.province.name

    def get_property_size_ha(self, obj: AnnualPopulation) -> str:
        return (
            round(obj.property.property_size_ha, 2) if
            obj.property.property_size_ha else 0
        )

    def get_open_close_systems(self, obj: AnnualPopulation) -> str:
        return obj.property.open.name if obj.property.open else ""

    def get_area_available_to_species(self, obj: AnnualPopulation) -> str:
        data = AnnualPopulation.objects.filter(
            taxon=obj.taxon,
            property=obj.property,
            year=obj.year
        ).aggregate(Sum('area_available_to_species'))
        return (
            round(data['area_available_to_species__sum'], 2) if
            data['area_available_to_species__sum'] else 0
        )

    class Meta:
        model = AnnualPopulation
        fields = [
            "property_name",
            "property_short_code",
            "organisation_name",
            "organisation_short_code",
            "year",
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

    def get_scientific_name(self, obj: AnnualPopulationPerActivity) -> str:
        return obj.annual_population.taxon.scientific_name

    def get_common_name(self, obj: AnnualPopulationPerActivity) -> str:
        return obj.annual_population.taxon.common_name_verbatim

    def get_property_name(self, obj: AnnualPopulationPerActivity) -> str:
        return obj.annual_population.property.name

    def get_property_short_code(self, obj: AnnualPopulationPerActivity) -> str:
        return obj.annual_population.property.short_code

    def get_organisation_name(self, obj: AnnualPopulationPerActivity) -> str:
        return obj.annual_population.property.organisation.name

    def get_organisation_short_code(
        self,
        obj: AnnualPopulationPerActivity
    ) -> str:
        return obj.annual_population.property.organisation.short_code

    def __init__(self, *args, **kwargs):
        activity = kwargs.pop('activity', None)
        if not activity:
            raise ValueError("'activity' argument is required!")
        super().__init__(*args, **kwargs)

        base_fields = [
            "property_name",
            "property_short_code",
            "organisation_name",
            "organisation_short_code",
            "scientific_name", "common_name",
            "year", "total", "adult_male", "adult_female",
            "juvenile_male", "juvenile_female"
        ]
        valid_fields = base_fields + activity.export_fields
        allowed = set(valid_fields)
        existing = set(self.fields.keys())
        for field_name in existing - allowed:
            self.fields.pop(field_name)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        count_fields = [
            "total", "adult_male", "adult_female",
            "juvenile_male", "juvenile_female"
        ]
        for k, v in representation.items():
            if k not in count_fields:
                continue
            representation[k] = 'NA' if v is None else v
        return representation

    class Meta:
        model = AnnualPopulationPerActivity
        fields = '__all__'


class NationalLevelSpeciesReport(serializers.Serializer):

    def to_representation(self, instance):
        del instance['taxon__common_name_verbatim']
        del instance['taxon__scientific_name']
        return instance


class NationalLevelPropertyReport(serializers.Serializer):

    def to_representation(self, instance):
        all_data = {}
        filters = self.context['filters']
        activity_field = (
            'annualpopulationperactivity__activity_type_id__in'
        )
        activity_filter = None
        if activity_field in filters:
            activity_filter = filters[activity_field]
            del filters[activity_field]
        property_data = AnnualPopulation.objects.filter(
            **filters, taxon=instance
        )
        if activity_filter:
            property_data = property_data.filter(activity_filter)
        property_data = property_data.values(
            "property__property_type__name",
            "year",
        ).annotate(
            population=Sum("total"),
            area=Sum("property__property_size_ha")
        ).order_by('-year')

        property_type_fields = set()
        property_area_fields = set()

        for property_entry in property_data:
            property_name = property_entry["property__property_type__name"]
            property_type_field = f"total_population_{property_name}_property"
            property_area_field = f"total_area_{property_name}_property"
            year = int(property_entry["year"])
            data = {
                "year": year,
                "common_name": (
                    instance.common_name_verbatim if
                    instance.common_name_verbatim else '-'
                ),
                "scientific_name": instance.scientific_name,
                property_type_field: property_entry["population"],
                property_area_field: property_entry["area"]
            }
            property_type_fields.add(property_type_field)
            property_area_fields.add(property_area_field)
            if year in all_data:
                all_data[year].update(data)
            else:
                all_data[year] = data

        all_data = [dt for dt in all_data.values()]
        for data in all_data:
            dt_type_fields = {
                key for key in data.keys() if
                key.startswith('total_population')
            }
            dt_area_fields = {
                key for key in data.keys() if
                key.startswith('total_area')
            }
            data.update(
                {
                    key: 0 for key in property_type_fields.difference(
                        dt_type_fields
                    )
                }
            )
            data.update(
                {
                    key: 0 for key in property_area_fields.difference(
                        dt_area_fields
                    )
                }
            )

        return all_data


class NationalLevelActivityReport(serializers.Serializer):

    def to_representation(self, instance):
        all_data = {}
        activity_data = AnnualPopulationPerActivity.objects.values(
            "activity_type__name",
            "year"
        ).filter(
            **self.context['filters'],
            annual_population__taxon=instance
        ).annotate(
            population=Sum("total"),
        ).order_by('-year')

        activity_fields = set()
        for activity_entry in activity_data:
            year = activity_entry["year"]
            activity_name = activity_entry[
                "activity_type__name"
            ]
            activity_field = f"total_population_{activity_name}"
            if not activity_name:
                continue

            data = {
                "year": activity_entry["year"],
                "common_name": instance.common_name_verbatim,
                "scientific_name": instance.scientific_name,
                activity_field: activity_entry["population"],
            }
            activity_fields.add(activity_field)
            if year in all_data:
                all_data[year].update(data)
            else:
                all_data[year] = data

        all_data = [dt for dt in all_data.values()]
        for data in all_data:
            dt_prov_fields = {
                key for key in data.keys() if
                key.startswith('total_population')
            }
            data.update(
                {key: 0 for key in activity_fields.difference(dt_prov_fields)}
            )

        return all_data


class NationalLevelProvinceReport(serializers.Serializer):

    def to_representation(self, instance):
        all_data = {}
        filters = self.context['filters']
        activity_field = (
            'annualpopulationperactivity__activity_type_id__in'
        )
        activity_filter = None
        if activity_field in filters:
            activity_filter = filters[activity_field]
            del filters[activity_field]
        province_data = AnnualPopulation.objects.select_related(
            'property__province'
        ).filter(
            **filters, taxon=instance
        )
        if activity_filter:
            province_data = province_data.filter(activity_filter)
        province_data = province_data.order_by('-year')

        province_fields = set()

        for province_entry in province_data:
            data = {
                "year": province_entry.year,
                "common_name": instance.common_name_verbatim,
                "scientific_name": instance.scientific_name,
            }
            year = province_entry.year
            province_name = province_entry.property.province.name
            province_field = f"total_population_{province_name}"
            data[province_field] = province_entry.total
            province_fields.add(province_field)
            if year in all_data:
                if province_field in all_data[year]:
                    all_data[year][province_field] += province_entry.total
                else:
                    all_data[year][province_field] = province_entry.total
            else:
                all_data[year] = data

        all_data = [dt for dt in all_data.values()]
        for data in all_data:
            dt_prov_fields = {
                key for key in data.keys() if
                key.startswith('total_population')
            }
            data.update(
                {key: 0 for key in province_fields.difference(dt_prov_fields)}
            )

        return all_data
