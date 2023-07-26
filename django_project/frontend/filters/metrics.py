import django_filters
from species.models import Taxon


class SpeciesPopulationCountFilter(django_filters.FilterSet):
    species = django_filters.CharFilter(method ='filter_species')
    start_year = django_filters.CharFilter(method ='filter_start_year')
    month = django_filters.CharFilter(method = 'filter_month')


    class Meta:
        model = Taxon
        fields = ['species', 'start_year', 'month']

    def filter_species(self, queryset, name, value):
        species_list = value.split(',')
        return queryset.filter(common_name_varbatim__in=species_list)

    def filter_month(self, queryset, name, value):
        month = value.split(',')
        start_year = self.data.get('start_year')
        end_year = self.data.get('end_year')
        return queryset.filter(
            ownedspecies__annualpopulationperactivity__month__name__in=month,
            ownedspecies__annualpopulationperactivity__year__range=(
                start_year, end_year
            )
        )

    def filter_start_year(self, queryset, name, value):
        start_year = int(value)
        end_year = int(self.data.get('end_year'))
        return queryset.filter(
            ownedspecies__annualpopulationperactivity__year__range=(
                start_year, end_year
            )
        )


class ActivityPercentageFilter(django_filters.FilterSet):
    species = django_filters.CharFilter(method ='filter_species')
    start_year = django_filters.CharFilter(method ='filter_start_year')
    property = django_filters.CharFilter(method = 'filter_property')


    class Meta:
        model = Taxon
        fields = ['species', 'start_year', 'property']

    def filter_species(self, queryset, name, value):
        species_list = value.split(',')
        return queryset.filter(common_name_varbatim__in=species_list)

    def filter_start_year(self, queryset, name, value):
        start_year = int(value)
        end_year = int(self.data.get('end_year'))
        return queryset.filter(
            ownedspecies__annualpopulationperactivity__year__range=(
                start_year,
                end_year
            )
        )

    def filter_property(self, queryset, name, value):
        properties_list = value.split(',')
        return queryset.filter(
            ownedspecies__property__name__in=properties_list
        )
