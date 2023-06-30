from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from species.models import Taxon
from frontend.serializers.species import TaxonSerializer
# Create your views here.
    
class TaxonViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        taxon = Taxon.objects.all()

        specie = self.request.query_params.get("species")
        if specie:
            search_value = specie.split(',')
            taxon = Taxon.objects.filter(common_name_varbatim__in=search_value)

        return Response(
            status=200,
            data=TaxonSerializer(taxon, many=True).data
        )