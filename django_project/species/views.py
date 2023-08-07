from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Taxon
from .serializers import TaxonSerializer
from django.views.generic import TemplateView



class TaxonListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        taxon = Taxon.objects.filter(taxon_rank__name="Species")
        return Response(
            status=200,
            data=TaxonSerializer(taxon, many=True).data
        )



class SpeciesForm(TemplateView):
    template_name  = 'species_form.html'