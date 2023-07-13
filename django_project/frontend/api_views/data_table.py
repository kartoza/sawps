from frontend.filters.data_table import OwnedSpeciesFilter
from frontend.serializers.data_table import OwnedSpeciesSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from species.models import OwnedSpecies


class DataTableAPIView(APIView):
    permission_classes = [IsAuthenticated]
    filter_class = OwnedSpeciesFilter

    def get_queryset(self):
        organisation_id = self.request.session.get('current_organisation_id')
        queryset = OwnedSpecies.objects.select_related('property').filter(
            property__organisation_id=organisation_id
        )
        filtered_queryset = OwnedSpeciesFilter(
            self.request.GET, queryset=queryset
        ).qs
        return filtered_queryset

    def get(self, request):
        queryset = self.get_queryset()
        serializer = OwnedSpeciesSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)
