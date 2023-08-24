"""API View related to national report
statistics
"""
from typing import List
from property.models import Property
from frontend.serializers.national_statistics import (
    NationalStatisticsSerializer,
    SpeciesListSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from species.models import OwnedSpecies, Taxon
from django.db.models import Count, Sum


class NationalSpeciesView(APIView): 
    """
    An API view to retrieve
    the statics for the national report
    """

    permission_classes = [IsAuthenticated]
    serializer_class = SpeciesListSerializer

    def get_species_list(self) -> List[Taxon]:
        """
        Returns a filtered queryset
        of Taxon objects representing
        species
        """
        queryset = Taxon.objects.filter(
            taxon_rank__name='Species'
        ).distinct()
        return queryset 

    def get(self,*args, **kwargs) -> Response:
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
    the statics for the national report
    """

    permission_classes = [IsAuthenticated]
    serializer_class = NationalStatisticsSerializer
    
    def get_statistics(self, request):
        """
        This method calculates the property
        count ,total property area and
        total property area available for
        owned species (national
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
 

    def get(self,*args, **kwargs) -> Response:
        """
        Handles the request
        and returns a serialized JSON response.
        """
        statistics = self.get_statistics(self.request)
        serializer = NationalStatisticsSerializer(statistics)
        return Response(serializer.data)
