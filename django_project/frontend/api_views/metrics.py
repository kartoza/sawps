from frontend.filters.metrics import SpeciesPopulationCountFilter
from frontend.serializers.metrics import (
    SpeciesPopulationCountSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from species.models import Taxon


class SpeciesPopulationCountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SpeciesPopulationCountSerializer

    def get_queryset(self, property_id):
        organisation_id = self.request.session.get('current_organisation_id')
        queryset = Taxon.objects.filter(
            ownedspecies__property__organisation_id=organisation_id,
            taxon_rank__name='Species', ownedspecies__property_id=property_id
        ).distinct()
        filtered_queryset = SpeciesPopulationCountFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset

    def get(self, request, property_id, *args, **kwargs):
        queryset = self.get_queryset(property_id=property_id)
        serializer = self.serializer_class(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data)
