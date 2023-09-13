from typing import List, Dict
from django.db.models.query import QuerySet
from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity
)


def data_table_reports(queryset: QuerySet, request) -> List[Dict]:
    """
    Generate data table reports based on the user's request.
    Params:
        queryset (QuerySet): The initial queryset to generate reports from.
        request: The HTTP request object.
    """
    reports_list = request.GET.get("reports")
    reports = []

    if reports_list:
        reports_list = reports_list.split(",")
        report_functions = {
            "Activity_report": activity_report,
            "Property_report": property_report,
            "Sampling_report": sampling_report,
            "Species_population_report": species_report,
        }

        for report_name in reports_list:
            if report_name in report_functions:
                report_data = report_functions[report_name](queryset, request)
                reports.append(
                    {report_name: report_data}
                ) if report_data else []

    else:
        reports.append(
            {"Property_report": property_report(queryset, request)}
        )if property_report(queryset, request) else []

    return reports


def get_common_data(property: QuerySet, request) -> Dict:
    """
    Retrieve common data for a property based on species selection.
    Params:
        property (QuerySet): The property for which common data is retrieved.
        request: The HTTP request object.
    """
    species_list = request.GET.get("species")

    if species_list:
        species_list = species_list.split(",")
        species = property.ownedspecies_set.filter(
            taxon__common_name_varbatim__in=species_list
        ).values(
            "taxon__common_name_varbatim", "taxon__scientific_name"
        )
    else:
        species = property.ownedspecies_set.all().values(
            "taxon__common_name_varbatim", "taxon__scientific_name"
        )

    return {
        "property_name": property.name,
        "common_name": species[0]["taxon__common_name_varbatim"],
        "scientific_name": species[0]["taxon__scientific_name"]
    } if species else {}


def species_report(queryset: QuerySet, request) -> List:
    """
    Generate species reports based on the user's request.
    Params:
        queryset (QuerySet): Properties queryset to generate reports from.
        request: The HTTP request object.
    """
    species_population_reports = []
    filters = {}
    start_year = request.GET.get("start_year")
    if start_year:
        end_year = request.GET.get("end_year")
        filters["year__range"] = (start_year, end_year)

    for property in queryset:
        common_data = get_common_data(property, request)

        if not common_data:
            continue

        species_population_data = AnnualPopulation.objects.filter(
            **filters,
            owned_species__property__name=property.name,
            owned_species__taxon__common_name_varbatim=(
                common_data["common_name"]
            )
        ).values(
            "year", "group", "total", "adult_male", "adult_female",
            "juvenile_male", "juvenile_female", "sub_adult_male",
            "sub_adult_female"
        )

        species_population_reports.extend([
            {**common_data, **data} for data in species_population_data
        ])

    return species_population_reports


def property_report(queryset: QuerySet, request) -> List:
    """
    Generate property reports based on the user's request.
    Params:
        queryset (QuerySet): Properties queryset to generate reports from.
        request: The HTTP request object.
    """
    property_reports = []
    filters = {}
    start_year = request.GET.get("start_year")
    if start_year:
        end_year = request.GET.get("end_year")
        filters["annualpopulation__year__range"] = (start_year, end_year)

    for property in queryset:
        common_data = get_common_data(property, request)

        if not common_data:
            continue

        if filters:
            area_available_values = property.ownedspecies_set.filter(
                **filters
            ).values("area_available_to_species")
        else:
            area_available_values = property.ownedspecies_set.all().values(
                "area_available_to_species"
            )

        property_reports.extend([
            {
                "property_name": common_data["property_name"],
                "scientific_name": common_data["scientific_name"],
                "common_name": common_data["common_name"],
                "owner": property.created_by.first_name,
                "owner_email": property.owner_email,
                "property_type": property.property_type.name,
                "province": property.province.name,
                "property_size_ha": property.property_size_ha,
                "area_available_to_species": area_available[
                    "area_available_to_species"
                ],
                "open": property.open
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
    start_year = request.GET.get("start_year")
    if start_year:
        end_year = request.GET.get("end_year")
        filters["year__range"] = (start_year, end_year)

    for property in queryset:
        common_data = get_common_data(property, request)

        if not common_data:
            continue

        sampling_reports_data = AnnualPopulation.objects.filter(
            **filters,
            owned_species__property__name=property.name,
            owned_species__taxon__common_name_varbatim = (
                common_data["common_name"]
            ),
        ).values(
            "population_status", "population_estimate_category",
            "survey_method", "sampling_effort_coverage",
            "population_estimate_certainty",
        )

        sampling_reports.extend([
            {**common_data, **data} for data in sampling_reports_data
        ])

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

    activity_types = [
        "Planned_euthanasia", "Planned_hunt/cull", "Planned_translocation",
        "Unplanned/natural_deaths", "Unplanned/illegal_hunt"
    ]

    activity_data_map = {
        "Unplanned/illegal_hunt": [],
        "Planned_euthanasia": ["intake_permit"],
        "Planned_hunt/cull": ["intake_permit"],
        "Planned_translocation": [
            "intake_permit", "translocation_destination",
            "offtake_permit"
        ],
        "Unplanned/natural_deaths": [
            "translocation_destination", "founder_population",
            "reintroduction_source"
        ],
    }

    activity_reports = {
        activity: [] for activity in activity_types
    }
    for property in queryset:
        common_data = get_common_data(property, request)

        if not common_data:
            continue

        for activity_name in activity_types:

            if activity_name in activity_data_map:
                query_values = [
                    "year", "total", "adult_male", "adult_female",
                    "juvenile_male", "juvenile_female"
                ] + activity_data_map[activity_name]

                activity_data = AnnualPopulationPerActivity.objects.values(
                    *query_values
                ).filter(
                    **filters,
                    owned_species__taxon__common_name_varbatim=common_data[
                        "common_name"
                    ],
                    owned_species__property__name=property.name,
                    activity_type__name=activity_name.replace(
                        "_", " "
                    ) if activity_name != "Unplanned/illegal_hunt"
                    else activity_name
                )

                activity_reports[activity_name].extend([
                    {**common_data, **data} for data in activity_data
                ])

    activity_reports = {k: v for k, v in activity_reports.items() if v}

    return activity_reports
