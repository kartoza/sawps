import django_filters
from django.db.models import Q

from species.models import OwnedSpecies


class OwnedSpeciesFilter(django_filters.FilterSet):
    species = django_filters.CharFilter(method ='filter_species')
    property = django_filters.CharFilter(method ='filter_property')
    month = django_filters.CharFilter(method = 'filter_month')
    activity_type = django_filters.CharFilter(method = 'filter_activity_type')
    population_category = django_filters.CharFilter(
        method = 'filter_population_category'
    )

    class Meta:
        model = OwnedSpecies
        fields = ['species', 'property', 'month']

    def filter_species(self, queryset, name, value):
        species_list = value.split(',')
        return queryset.filter(taxon__common_name_varbatim__in=species_list)

    def filter_property(self, queryset, name, value):
        property_list = value.split(',')
        return queryset.filter(property__name__in=property_list)

    def filter_month(self, queryset, name, value):
        month = value.split(',')
        start_year = self.data.get('start_year')
        end_year = self.data.get('end_year')
        return queryset.filter(
            annualpopulation__month__name__in=month,
            annualpopulation__year__range=(start_year, end_year)
        )

    def filter_population_category(self, queryset, name, value):
        population_category = value.split(',')
        ranges = [range.split('-') for range in population_category]
        query = Q()
        for range_values in ranges:
            query |= Q(
                annualpopulation__total__range=(
                range_values[0], range_values[1]
                )
            )
        return queryset.filter(query)

    def filter_activity_type(self, queryset, name, value):
        activity_type = value.split(',')
        return queryset.filter(
            annualpopulationperactivity__activity_type__name__in=activity_type
        )
