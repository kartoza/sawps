from collections import Counter
from typing import Dict, List, Any

from frontend.static_mapping import ACTIVITY_COLORS_DICT
from django.db.models import QuerySet, Sum
from property.models import Property
from species.models import OwnedSpecies
from population_data.models import AnnualPopulation


def calculate_population_categories(queryset: QuerySet) -> Dict[str, int]:
    """
    Calculate population categories for a given queryset of properties.

    Args:
        queryset (QuerySet): A Django QuerySet containing Property objects.

    Returns:
        Dict[str, int]: A dictionary containing population categories
        as keys and their corresponding counts as values.

    """

    population_category_dict = {
        "1-10": 0,
        "11-20": 0,
        "21-50": 0,
        "51-100": 0,
        "101-200": 0,
        ">200": 0
    }

    property_ids = [query.id for query in queryset]

    property_population_totals = Property.objects.filter(
        id__in=property_ids
    ).annotate(
        population_total=Sum("ownedspecies__annualpopulation__total")
    ).values_list("id", "population_total")
    population_counter = Counter(
        "1-10" if (population is not None and 1 <= population <= 10) else
        "11-20" if (population is not None and 11 <= population <= 20) else
        "21-50" if (population is not None and 21 <= population <= 50) else
        "51-100" if (population is not None and 51 <= population <= 100) else
        "101-200" if (population is not None and 101 <= population <= 200)
        else
        ">200"
        for _, population in property_population_totals
    )

    population_category_dict.update(population_counter)

    return population_category_dict


def calculate_total_area_available_to_species(queryset: QuerySet[Property]) \
    -> List[Dict[str, int]]:
    """
    Calculate the total area available to species for
    each property in the queryset.

    Params:
        queryset (QuerySet[Property]): The queryset of properties for
        which to calculate total area available to species.

    Returns:
        List[Dict[str, int]]: A list of dictionaries,
        each containing the property name and
        the total area available to species for that property.
    """
    properties = []
    for property in queryset:
        property_data = OwnedSpecies.objects.values("property__name").filter(
            property=property
        ).annotate(
            total_species_area=Sum("area_available_to_species")
        ).values("property__name", "total_species_area").distinct()

        data = {
            "property_name": property_data[0]["property__name"].capitalize(),
            "area": property_data[0]["total_species_area"]
        }
        properties.append(data)

    return properties


def calculate_total_area_per_property_type(queryset: QuerySet) -> List[dict]:
    """
    Calculate the total area per property type
    for a given queryset of properties.
    Params:
        queryset (QuerySet): The queryset of Property objects.
    Returns:
        list[dict]: A list of dictionaries, each containing property_type
                    and total_area keys representing the property type name
                    and the aggregated total area respectively.
    """
    property_ids = queryset.values_list('id', flat=True)
    properties_type_area = Property.objects.filter(
        id__in=property_ids
    ).values('property_type__name').annotate(
        total_area=Sum('property_size_ha')
    ).values('property_type__name', 'total_area')
    return properties_type_area


def calculate_base_population_of_species(data: List[Dict[str, Any]]) \
    -> Dict[str, Any]:
    """
    Calculate base population of species and modify the input data.
    Params:
        data (List[Dict[str, Any]]): List of dictionaries
        representing species data.
    Returns:
        Dict[str, Any]: A dictionary containing modified species
        data with base percentages and activity colors.
    """
    calculated_data = []
    for species in data:
        activities_total = sum(
            activity["activity_total"] for activity in species["activities"]
        )
        if species["total"]:
            base = species["total"] - activities_total
            base_percentage = (
                base / species["total"]
            ) * 100 if base else None
            species["activities"].append({"Base population": base_percentage})
            calculated_data.append(species)
    species_data = {
        "data": calculated_data,
        "activity_colours": ACTIVITY_COLORS_DICT
    }
    return species_data

from django.db.models import Q, Sum

def calculate_totals_per_age_group(queryset, request):
    owned_species_ids = queryset.values_list("ownedspecies__id", flat=True)
    sum_fields = [
        "adult_male",
        "adult_female",
        "sub_adult_male",
        "sub_adult_female",
        "juvenile_male",
        "juvenile_female"
    ]

    filters = {
        "owned_species__id__in": owned_species_ids
    }

    property_list = request.GET.get("property")
    if property_list:
        property_ids = property_list.split(",")
        filters["owned_species__property__id__in"] = property_ids

    start_year = request.GET.get("start_year")
    if start_year:
        end_year = request.GET.get("end_year")
        filters["year__range"] = (start_year, end_year)

    age_groups_totals = AnnualPopulation.objects.filter(**filters).aggregate(
        **{f"total_{field}": Sum(field) for field in sum_fields}
    )
    return [age_groups_totals]
