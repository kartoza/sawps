from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Taxon
from .serializers import TaxonSerializer
# Create your views here.


class TaxonListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        taxon = Taxon.objects.filter(taxon_rank__name="Species")
        return Response(
            status=200,
            data=TaxonSerializer(taxon, many=True).data
        )
