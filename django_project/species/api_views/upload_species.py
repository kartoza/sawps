import csv
import codecs
from django.contrib.auth.models import User
from scripts.csv_headers import CSV_FILE_HEADERS
from swaps.models import UploadSession
from datetime import datetime
from django.http import JsonResponse
from species.serializers import FileUploadSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



class SpeciesUploader(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        finished = False

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        species_file = serializer.validated_data['file']

        if not species_file:
            return JsonResponse({
                'status': 'error',
                'message': 'CSV file not valide',
            })

        upload_session, e  = UploadSession.objects.get_or_create(
            success_file=''
        )
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
                return Response(
                    {"status": "Header row does not follow the correct format"},
                    status.HTTP_424_FAILED_DEPENDENCY
                )

        finished = True
        if finished:
            upload_session.uploader=self.request.user,
            upload_session.process_file=species_file,
            upload_session.uploaded_at=datetime.now(),
            uploaded_at=datetime.now(),
            upload_session.save()

            task = upload_species_data.delay(
                upload_session.id
            )

            upload_session.token = task.id
            upload_session.save()

            return Response({"status": "success"},
                        status.HTTP_201_CREATED)
