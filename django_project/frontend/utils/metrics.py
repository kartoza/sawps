from collections import Counter
from typing import Dict

from django.db.models import QuerySet, Sum
from property.models import Property


def calculate_population_categories(queryset: QuerySet) -> Dict[str, int]:
    """
    Calculate population categories for a given queryset of properties.

    This function takes a queryset of properties and calculates
    the distribution of property populations into predefined
    categories based on the total annual population of owned species.

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
