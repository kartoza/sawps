from typing import List
from activity.models import ActivityType
from population_data.models import AnnualPopulationPerActivity
from frontend.utils.metrics import calculate_population_categories
from frontend.filters.metrics import PropertyFilter
from property.models import Property, PropertyType
from frontend.serializers.national_statistics import (
    NationalStatisticsSerializer,
    SpeciesListSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from species.models import OwnedSpecies, Taxon
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.db.models import Q
from django.db.models.functions import Coalesce


class NationalSpeciesView(APIView):
    """
    An API view to retrieve
    the statistics for the national report.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = SpeciesListSerializer

    def get_species_list(self) -> List[Taxon]:
        """
        Returns a filtered queryset
        of Taxon objects representing
        species.
        """
        queryset = Taxon.objects.filter(
            taxon_rank__name='Species'
        ).distinct()
        return queryset

    def get(self, *args, **kwargs) -> Response:
        """
        Handles the request
        and returns a serialized JSON response.
        """
        queryset = self.get_species_list()
        serializer = SpeciesListSerializer(
            queryset, many=True,
        )
        return Response(serializer.data)


class NationalStatisticsView(APIView):
    """
    An API view to retrieve
    the statistics for the national report.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = NationalStatisticsSerializer

    def get_statistics(self, request):
        """
        This method calculates the property
        count, total property area, and
        total property area available for
        owned species (national).
        """
        organisation_id = request.session.get(
            'current_organisation_id'
        )

        national_properties = Property.objects.filter(
            property_type__name='national',
            organisation=organisation_id
        )

        # Count the number of matching properties
        total_property_count = national_properties.count()

        # Sum up the property sizes to get total area available
        total_property_area = national_properties.aggregate(
            total_area=Sum('property_size_ha')
        )['total_area']

        # Query the OwnedSpecies table and
        # get the area available to species for each property
        property_ids = national_properties.values_list('id', flat=True)
        total_area_available_to_species = OwnedSpecies.objects.filter(
            property__id__in=property_ids
        ).aggregate(
            total_area_to_species=Sum('area_available_to_species')
        )['total_area_to_species']

        # Create a dictionary with the aggregated values
        aggregated_data = {
            'total_property_count': total_property_count,
            'total_property_area': total_property_area,
            'total_area_available_to_species': total_area_available_to_species,
        }

        return aggregated_data

    def get(self, *args, **kwargs) -> Response:
        """
        Handles the request
        and returns a serialized JSON response.
        """
        statistics = self.get_statistics(self.request)
        serializer = NationalStatisticsSerializer(statistics)
        return Response(serializer.data)


class NationalPropertiesView(APIView):
    """
    An API view to retrieve
    the statistics for the national report.
    """

    permission_classes = [IsAuthenticated]

    def get_properties_per_population_category(self) -> QuerySet[Property]:
        """
        Get the filtered queryset
        of properties owned by the organization.
        """
        organisation_id = self.request.session.get(
            'current_organisation_id'
        )
        property_type = PropertyType.objects.filter(
            Q(name__iexact='national')
        ).first()
        queryset = Property.objects.filter(
            organisation_id=organisation_id,
            property_type=property_type
        )
        filtered_queryset = PropertyFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset

    def get(self, *args, **kwargs) -> Response:
        """
        Handle GET request to
        retrieve population categories for properties.
        """
        queryset = self.get_properties_per_population_category()
        return Response(calculate_population_categories(queryset))


class NationalActivityCountView(APIView):
    """
    API to retrieve activity count as % of the
    the total population for each species
    """

    permission_classes = [IsAuthenticated]

    def get_activity_count(self) -> QuerySet[Property]:
        """
        Get activity count of the total
        population as percentage
        """
        organisation_id = self.request.session.get(
            'current_organisation_id'
        )
        property_type = PropertyType.objects.filter(
            name__iexact='national'
        ).first()
        properties = Property.objects.filter(
            organisation_id=organisation_id,
            property_type=property_type
        )

        # Retrieve species on each property
        species_per_property = OwnedSpecies.objects.filter(
            property__in=properties
        ).values('taxon', 'property')

        # Retrieve activity types
        activity_types = ActivityType.objects.all()

        # Retrieve population count
        # for each species and activity type
        population_counts = []
        for species in species_per_property:
            for activity_type in activity_types:
                population_count = AnnualPopulationPerActivity.objects.filter(
                    owned_species__taxon=species['taxon'],
                    activity_type=activity_type
                ).aggregate(
                    population_count=Coalesce(Sum('total'), 0)
                )['population_count']

                population_counts.append({
                    'species': species['taxon'],
                    'activity_type': activity_type.name,
                    'population_count': population_count
                })

        # Calculate the total population count per species
        total_population_per_species = {}
        for item in population_counts:
            species = item['species']
            population_count = item['population_count']
            if species in total_population_per_species:
                total_population_per_species[species] += population_count
            else:
                total_population_per_species[species] = population_count

        # Calculate the percentage of each species for each activity type
        result = {}
        for item in population_counts:
            species = item['species']
            activity_type = item['activity_type']
            population_count = item['population_count']
            total_population = total_population_per_species[species]
            percentage = (
                population_count / total_population
            ) * 100 if total_population != 0 else 0


            taxa = OwnedSpecies.objects.filter(id=species).first()
            if taxa:
                taxon = taxa.taxon
                common_name = taxon.common_name_varbatim
                icon_url = taxon.icon.url if taxon.icon else None

            else:
                common_name = 'None'
                icon_url = None
            if species not in result:
                result[species] = {
                    'species_name': common_name,
                    'icon': icon_url
                }
            result[species][activity_type] = f'{percentage:.2f}%'

        return result

    def get(self, *args, **kwargs) -> Response:
        """
        Handle GET request to
        retrieve population categories for properties.
        """
        queryset = self.get_activity_count()
        return Response(queryset)
