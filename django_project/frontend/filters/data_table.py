import django_filters
from species.models import OwnedSpecies


class OwnedSpeciesFilter(django_filters.FilterSet):
    species = django_filters.CharFilter(method ='filter_species')
    property = django_filters.CharFilter(method ='filter_property')
    month = django_filters.CharFilter(method = 'filter_month')

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
        start_year = self.data['start_year']
        end_year = self.data['end_year']
        queryset = queryset.filter(
            annualpopulation__month__name__in=month,
            annualpopulation__year__range=(start_year, end_year)
        )
        return queryset
