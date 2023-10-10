import urllib.parse
from typing import Dict, List
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.http import HttpRequest
from frontend.utils.organisation import get_current_organisation_id
from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity
)
from population_data.serializers import OpenCloseSystemSerializer
from property.models import Province, Property
from species.models import OwnedSpecies

ACTIVITY_REPORT = 'Activity_report'
PROPERTY_REPORT = 'Property_report'
SAMPLING_REPORT = 'Sampling_report'
SPECIES_REPORT = 'Species_report'
PROVINCE_REPORT = 'Province_report'


def data_table_reports(queryset: QuerySet, request) -> List[Dict]:
    """
    Generate data table reports based on the user's request.
    Params:
        queryset (QuerySet): The initial queryset to generate reports from.
        request: The HTTP request object.
    """
    reports_list = request.GET.get("reports", None)
    reports = []

    if reports_list:
        reports_list = reports_list.split(",")
        report_functions = {
            ACTIVITY_REPORT: activity_report,
            PROPERTY_REPORT: property_report,
            SAMPLING_REPORT: sampling_report,
            SPECIES_REPORT: species_report,
        }

        for report_name in reports_list:
            if report_name in report_functions:
                report_data = report_functions[report_name](queryset, request)
                reports.append(
                    {report_name: report_data}
                ) if report_data else []

    else:
        property_report_data = property_report(queryset, request)
        if property_report_data:
            reports.append({PROPERTY_REPORT: property_report_data})

    return reports


def species_report(queryset: QuerySet, request) -> List:
    """
    Generate species reports based on the user's request.
    Params:
        queryset (QuerySet): Properties queryset to generate reports from.
        request: The HTTP request object.
    """
    species_reports = []
    filters = {}
    selected_fields = [
        "owned_species__property__name",
        "owned_species__taxon__scientific_name",
        "owned_species__taxon__common_name_varbatim",
        "year", "group", "total", "adult_male", "adult_female",
        "juvenile_male", "juvenile_female", "sub_adult_male",
        "sub_adult_female",
    ]

    species_list = request.GET.get("species")
    if species_list:
        species_list = species_list.split(",")
        filters["owned_species__taxon__scientific_name__in"] = species_list

    start_year = request.GET.get("start_year")
    if start_year:
        end_year = request.GET.get("end_year")
        filters["year__range"] = (start_year, end_year)

    activity = request.GET.get("activity")
    if activity:
        activity = urllib.parse.unquote(activity)
        filters[
            "owned_species__annualpopulationperactivity__activity_type__name"
        ] = activity

    for property in queryset:
        species_population_data = AnnualPopulation.objects.filter(
            **filters, owned_species__property__name=property.name,
        ).values(*selected_fields).distinct()

        species_reports.extend(species_population_data)

    return species_reports


def property_report(queryset: QuerySet, request) -> List:
    """
    Generate property reports based on the user's request.
    Params:
        queryset (QuerySet): Properties queryset to generate reports from.
        request: The HTTP request object.
    """
    property_reports = []
    filters = {}

    species_list = request.GET.get("species")
    if species_list:
        species_list = species_list.split(",")
        filters["taxon__scientific_name__in"] = species_list

    start_year = (request.GET.get("start_year"))
    if start_year:
        end_year = int(request.GET.get("end_year"))
        start_year = int(request.GET.get("start_year"))
        filters["annualpopulation__year__range"] = (start_year, end_year)

    activity = request.GET.get("activity")
    if activity:
        activity = urllib.parse.unquote(activity)
        filters[
            "annualpopulationperactivity__activity_type__name"
        ] = activity

    for property in queryset:
        area_available_values = property.ownedspecies_set.filter(
            **filters
        ).values(
            "area_available_to_species",
            "taxon__scientific_name",
            "taxon__common_name_varbatim"
        )

        property_reports.extend([
            {
                "property_name": property.name,
                "scientific_name": area_available["taxon__scientific_name"],
                "common_name": area_available["taxon__common_name_varbatim"],
                "owner": property.created_by.first_name,
                "owner_email": property.owner_email,
                "property_type": property.property_type.name,
                "province": property.province.name,
                "property_size_ha": property.property_size_ha,
                "area_available_to_species": area_available[
                    "area_available_to_species"
                ],
                "open_close_system": OpenCloseSystemSerializer(
                    property.open
                ).data['name'] if property.open else None
            }
            for area_available in area_available_values
        ])

    return property_reports


def sampling_report(queryset: QuerySet, request) -> List:
    """
    Generate sampling reports based on the user's request.
    Params:
        queryset (QuerySet): Properties queryset to generate reports from.
        request: The HTTP request object.
    """
    sampling_reports = []
    filters = {}
    select_fields = [
            "owned_species__property__name",
            "owned_species__taxon__scientific_name",
            "owned_species__taxon__common_name_varbatim",
            "population_status__name",
            "population_estimate_category__name",
            "survey_method__name",
            "sampling_effort_coverage__name",
            "population_estimate_certainty",
    ]

    start_year = request.GET.get("start_year")
    if start_year:
        end_year = request.GET.get("end_year")
        filters["year__range"] = (start_year, end_year)

    activity = request.GET.get("activity")
    if activity:
        activity = urllib.parse.unquote(activity)
        filters[
            "owned_species__annualpopulationperactivity__activity_type__name"
        ] = activity

    species_list = request.GET.get("species")
    if species_list:
        species_list = species_list.split(",")
        filters["owned_species__taxon__scientific_name__in"] = species_list

    for property in queryset:

        sampling_reports_data = AnnualPopulation.objects.filter(
            **filters, owned_species__property__name=property.name,
        ).values(*select_fields)

        sampling_reports.extend(sampling_reports_data)

    return sampling_reports


def activity_report(queryset: QuerySet, request) -> Dict[str, List[Dict]]:
    """
    Generate property reports based on the user's request.
    Params:
        queryset (QuerySet): Properties queryset to generate reports from.
        request: The HTTP request object.
    """
    filters = {}
    start_year = request.GET.get("start_year")
    if start_year:
        end_year = request.GET.get("end_year")
        filters["year__range"] = (start_year, end_year)

    activity = request.GET.get("activity")
    if activity:
        activity_types = [urllib.parse.unquote(activity)]
    else:
        activity_types = [
            "Planned euthanasia", "Planned hunt/cull",
            "Planned translocation", "Unplanned/natural deaths",
            "Unplanned/illegal hunting"
        ]

    species_list = request.GET.get("species")
    if species_list:
        species_list = species_list.split(",")
        filters["owned_species__taxon__scientific_name__in"] = species_list

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

    activity_reports = {
        activity: [] for activity in activity_types
    }

    for property in queryset:

        for activity_name in activity_types:

            if activity_name in activity_data_map:
                query_values = [
                    "owned_species__property__name",
                    "owned_species__taxon__scientific_name",
                    "owned_species__taxon__common_name_varbatim",
                    "year", "total", "adult_male", "adult_female",
                    "juvenile_male", "juvenile_female",
                ] + activity_data_map[activity_name]

                activity_data = AnnualPopulationPerActivity.objects.values(
                    *query_values,
                ).filter(
                    **filters,
                    owned_species__property__name=property.name,
                    activity_type__name=activity_name
                )
                activity_reports[activity_name].extend(activity_data)

    activity_reports = {k: v for k, v in activity_reports.items() if v}

    return activity_reports


def national_level_user_table(
        queryset: QuerySet, request: HttpRequest, role: str
) -> List[Dict]:
    """
    Generate national-level reports for a user based on their role.

    Params:
        queryset : The initial queryset for data retrieval.
        request : The HTTP request object containing query parameters.
        role : The role of the user.
    """
    reports_list = request.GET.get("reports")
    reports = []
    if reports_list:
        reports_list = reports_list.split(",")
        report_functions = {
            PROPERTY_REPORT: national_level_property_report,
            ACTIVITY_REPORT: national_level_activity_report,
            SPECIES_REPORT: national_level_species_report,
        }

        if role != "Regional data consumer":
            report_functions[
                PROVINCE_REPORT
            ] = national_level_province_report

        for report_name in reports_list:
            if report_name in report_functions:
                report_data = report_functions[
                    report_name
                ](queryset, request, role)
                if report_data:
                    reports.append({report_name: report_data})

    else:
        data = national_level_property_report(queryset, request, role)
        if data:
            reports.append({PROPERTY_REPORT: data})

    return reports


def common_filters(request: HttpRequest, role: str) -> Dict:
    """
    Generate common filters for data retrieval based on
    the user's role and request parameters.

    Params:
        request : The HTTP request object containing query parameters.
        role : The role of the user.
    """
    filters = {}
    properties = Property.objects.all()

    start_year = request.GET.get("start_year")
    if start_year:
        end_year = request.GET.get("end_year")
        filters["annualpopulation__year__range"] = (
            start_year, end_year
        )

    property_param = request.GET.get("property")
    if property_param:
        properties = properties.filter(
            id__in=property_param.split(',')
        )

    spatial_filter_values = request.GET.get(
        'spatial_filter_values',
        ''
    ).split(',')

    spatial_filter_values = list(
        filter(None, spatial_filter_values)
    )

    if spatial_filter_values:
        properties = properties.filter(
            **({
                'spatialdatamodel__spatialdatavaluemodel__'
                'context_layer_value__in':
                    spatial_filter_values
            })
        )

    activity = request.GET.get("activity")
    if activity:
        filters[
            "annualpopulationperactivity__activity_type__name"
        ] = urllib.parse.unquote(activity)

    if role == "Regional data consumer":
        organisation_id = get_current_organisation_id(
            request.user
        )
        province_ids = Province.objects.filter(
            property__organisation_id=organisation_id
        ).values_list("id", flat=True)
        properties = properties.filter(
            province__id__in=province_ids
        )

    filters['property__id__in'] = list(
        properties.values_list('id', flat=True)
    )

    return filters


def national_level_species_report(
        queryset: QuerySet, request: HttpRequest, role: str
) -> List[Dict]:
    """
    Generate a national-level species report based on
    the provided queryset and request parameters.

    Args:
        queryset : The initial queryset containing species data.
        request : The HTTP request object containing query parameters.
        role : The role of the user.

    """
    filters = common_filters(request, role)
    report_data = []

    for species in queryset:
        report_data.extend(OwnedSpecies.objects.values("taxon").filter(
                **filters, taxon=species).annotate(
            propert_area=Sum("property__property_size_ha"),
            total_area_available=Sum("area_available_to_species"),
            adult_male_total_population=Sum(
                "annualpopulation__adult_male"
            ),
            adult_female_total_population=Sum(
                "annualpopulation__adult_female"
            ),
            sub_adult_male_total_population=Sum(
                "annualpopulation__sub_adult_male"
            ),
            sub_adult_female_total_population=Sum(
                "annualpopulation__sub_adult_female"
            ),
            juvenile_male_total_population=Sum(
                "annualpopulation__juvenile_male"
            ),
            juvenile_female_total_population=Sum(
                "annualpopulation__juvenile_female"
            ),
        ).values(
            "taxon__common_name_varbatim",
            "taxon__scientific_name",
            "propert_area",
            "total_area_available",
            "adult_male_total_population",
            "adult_female_total_population",
            "sub_adult_male_total_population",
            "sub_adult_female_total_population",
            "juvenile_male_total_population",
            "juvenile_female_total_population",
        ))
    return report_data


def national_level_property_report(
        queryset: QuerySet, request: HttpRequest, role: str
) -> List[Dict]:
    """
    Generate a national-level property report based on
    the provided queryset and request parameters.

    Args:
        queryset : The initial queryset containing species data.
        request : The HTTP request object containing query parameters.
        role : The role of the user.

    """
    filters = common_filters(request, role)
    report_data = []

    for species in queryset:
        data = {
            "common_name": (
                species.common_name_varbatim if
                species.common_name_varbatim else '-'
            ),
            "scientific_name": species.scientific_name,
        }

        property_data = OwnedSpecies.objects.values(
            "property__property_type__name",
        ).filter(**filters, taxon=species).annotate(
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

        report_data.append(data)

    return report_data


def national_level_activity_report(
        queryset: QuerySet, request: HttpRequest, role: str
) -> List[Dict]:
    """
    Generate a national-level activity report based on
    the provided queryset and request parameters.

    Args:
        queryset : The initial queryset containing species data.
        request : The HTTP request object containing query parameters.
        role : The role of the user.

    """
    filters = {}

    start_year = request.GET.get("start_year")
    if start_year:
        end_year = request.GET.get("end_year")
        filters[
            "annualpopulationperactivity__year__range"
        ] = (start_year, end_year)

    property_param = request.GET.get("property")
    if property_param:
        property_list = property_param.split(",")
        filters["property__id__in"] = property_list

    if role == "Regional data consumer":
        organisation_id = get_current_organisation_id(request.user)
        province_ids = Province.objects.filter(
            property__organisation_id=organisation_id
        ).values_list("id", flat=True)
        filters["property__province__id__in"] = province_ids

    report_data = []

    for species in queryset:
        data = {
            "common_name": species.common_name_varbatim,
            "scientific_name": species.scientific_name,
        }

        activity_data = OwnedSpecies.objects.values(
            "annualpopulationperactivity__activity_type__name",
        ).filter(**filters, taxon=species).annotate(
            population=Sum("annualpopulationperactivity__total"),
        )

        for activity_entry in activity_data:
            activity_name = activity_entry[
                "annualpopulationperactivity__activity_type__name"
            ]
            data[
                f"total_population_{activity_name}"
            ] = activity_entry["population"]

        report_data.append(data)

    return report_data


def national_level_province_report(
        queryset: QuerySet, request: HttpRequest, role: str
) -> List[Dict]:
    """
    Generate a national-level species report based on
    the provided queryset and request parameters.

    Args:
        queryset : The initial queryset containing species data.
        request : The HTTP request object containing query parameters.
        role : The role of the user.

    """
    filters = common_filters(request, role)
    report_data = []

    for species in queryset:
        data = {
            "common_name": species.common_name_varbatim,
            "scientific_name": species.scientific_name,
        }

        province_data = OwnedSpecies.objects.values(
            "property__province__name",
        ).filter(**filters, taxon=species).annotate(
            population=Sum("annualpopulation__total"),
        )

        for province_entry in province_data:
            province_name = province_entry["property__province__name"]
            data[
                f"total_population_{province_name}"
            ] = province_entry["population"]

        report_data.append(data)

    return report_data
