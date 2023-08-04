"""Filters in metrics.

"""
import django_filters
from django.db.models.query import QuerySet
from property.models import Property
from species.models import Taxon


class SpeciesPopulationCountFilter(django_filters.FilterSet):
    species = django_filters.CharFilter(method ='filter_species')
    start_year = django_filters.CharFilter(method ='filter_start_year')


    class Meta:
        model = Taxon
        fields = ['species', 'start_year']

    def filter_species(self, queryset, name, value):
        species_list = value.split(',')
        return queryset.filter(common_name_varbatim__in=species_list)


    def filter_start_year(self, queryset, name, value):
        start_year = int(value)
        end_year = int(self.data.get('end_year'))
        return queryset.filter(
            ownedspecies__annualpopulationperactivity__year__range=(
                start_year, end_year
            )
        )


class BaseMetricsFilter(django_filters.FilterSet):
    species = django_filters.CharFilter(method='filter_species')
    start_year = django_filters.CharFilter(method='filter_start_year')
    property = django_filters.CharFilter(method='filter_property')

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
            ownedspecies__property__id__in=properties_list
        )


class PropertyFilter(django_filters.FilterSet):
    """
    A custom filter for filtering Property objects based on
    a comma-separated list of property IDs.
    """
    property = django_filters.CharFilter(method='filter_property')

    class Meta:
        model = Property
        fields = ['property']

    def filter_property(self, queryset: QuerySet, value: str) -> QuerySet:
        """
        Custom filter method to filter properties by their IDs.
        params:
            queryset (QuerySet): The initial queryset of Property objects.
            value (str): A comma-separated list of property IDs.
        """
        properties_list = value.split(',')
        return queryset.filter(id__in=properties_list)
