import csv
import codecs
from scripts.csv_headers import CSV_FILE_HEADERS
from rest_framework.parsers import MultiPartParser
from frontend.models import UploadSpeciesCSV
from datetime import datetime
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from species.tasks.upload_species import upload_species_data



class SpeciesUploader(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        species_file = request.FILES['file']
        
        if not species_file:
            return Response(
                    {"status": "file is not correct"},
                    status.HTTP_424_FAILED_DEPENDENCY
                )
        
        upload_session = UploadSpeciesCSV.objects.create(
            process_file=species_file,
            uploader=self.request.user,
            uploaded_at=datetime.now(),
        )
        reader = csv.DictReader(codecs.iterdecode(species_file, 'utf-8'))
        headers = reader.fieldnames
        # check headers
        for header in CSV_FILE_HEADERS:
            if header not in headers:
                error_message = (
                    'Header row does not follow the correct format'
                )
                upload_session.error_notes = error_message
                upload_session.error_file = (
                    upload_session.process_file
                )
                upload_session.canceled = True
                upload_session.save()
                return Response(
                    {"status": "Header row does not follow the correct format"},
                    status.HTTP_424_FAILED_DEPENDENCY
                )

        task = upload_species_data.delay(
                upload_session.id
        )

        if task:
            return Response(status=200)
        
        return Response(status=404)

