from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Taxon
from .serializers import TaxonSerializer, FrontPageTaxonSerializer
from frontend.utils.organisation import (
    get_current_organisation_id
)
# Create your views here.


class TaxonListAPIView(APIView):
    """Get taxon within the organisations"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        organisation_id = get_current_organisation_id(self.request.user)

        organisation = self.request.GET.get("organisation") 
        if organisation:
            ids = organisation.split(",")
            taxon = Taxon.objects.filter(
                organisation_id__in=ids,
                ownedspecies__taxon__taxon_rank__name = "Species"
            )
        else:
            taxon = Taxon.objects.filter(
                organisation_id=organisation_id,
                taxon_rank__name="Species"
            )

        return Response(
            status=200,
            data=TaxonSerializer(taxon, many=True).data
        )


class TaxonFrontPageListAPIView(APIView):
    """Fetch taxon list to display on FrontPage."""
    permission_classes = [AllowAny]

    def get(self, request):
        taxon = Taxon.objects.filter(
            show_on_front_page=True).order_by('front_page_order')
        return Response(
            status=200,
            data=FrontPageTaxonSerializer(taxon, many=True).data
        )
