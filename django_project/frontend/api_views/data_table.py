from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from species.models import OwnedSpecies
from frontend.serializers.data_table import OwnedSpeciesSerializer
from frontend.filters.data_table import OwnedSpeciesFilter


class DataTableAPIView(APIView):
    permission_classes = [IsAuthenticated]
    filter_class = OwnedSpeciesFilter
    queryset = OwnedSpecies.objects.all()

    def get_queryset(self):
        queryset = OwnedSpeciesFilter(
            self.request.GET, queryset=self.queryset
        ).qs
        return queryset

    def get(self, request):
        queryset = self.get_queryset()
        serializer = OwnedSpeciesSerializer(
            queryset, many=True, context = {"request": request}
        )
        return Response(serializer.data)
