from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from tasks.upload_species import upload_species_data
from scripts.csv_headers import CSV_FILE_HEADERS
from swaps.models import UploadSession
from datetime import datetime
from django.http import JsonResponse



class SpeciesUploader(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        finished = False

from .models import Taxon
from .serializers import TaxonSerializer
# Create your views here.
        species_file = request.FILES.get('species-file')

        if not species_file:
            return JsonResponse({
                'status': 'error',
                'message': 'CSV file not valide',
            })

        upload_session  = UploadSession()
        reader = csv.DictReader(codecs.iterdecode(species_file, 'utf-8'))
        headers = reader.fieldnames
        # check headers
        for header in CSV_FILE_HEADERS:
            if header not in headers:
                error_message = (
                    'Header row does not follow the correct format'
                )
                upload_session.progress = error_message
                upload_session.error_file = (
                    upload_session.process_file
                )
                upload_session.processed = True
                upload_session.save()
                return False

        finished = True
        if finished:
            upload_session.update(
                uploader=self.request.user,
                process_file=species_file,
                uploaded_at=datetime.now(),
            )

            upload_session.save()

            task = upload_species_data.delay(
                upload_session.id,
                self.request.user.id
            )

            upload_session.token = task.id
            upload_session.save()

            return JsonResponse({
                'status': 'PENDING',
                'message': 'Processing',
                'task': upload_session.token
            })


class TaxonListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        taxon = Taxon.objects.filter(taxon_rank__name="Species")
        return Response(
            status=200,
            data=TaxonSerializer(taxon, many=True).data
        )
