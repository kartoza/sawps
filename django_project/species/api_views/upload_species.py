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
from frontend.tasks.parcel import boundary_files_search


class SpeciesUploader(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        # species_file = request.FILES['file']
        #
        # if not species_file:
        #     return JsonResponse({
        #         'status': 'error',
        #         'message': 'CSV file not valide',
        #     })
        #
        # upload_session = UploadSpeciesCSV.objects.create(
        #     process_file=species_file,
        #     uploader=self.request.user,
        #     uploaded_at=datetime.now(),
        # )
        # reader = csv.DictReader(codecs.iterdecode(species_file, 'utf-8'))
        # headers = reader.fieldnames
        # check headers
        # for header in CSV_FILE_HEADERS:
        #     if header not in headers:
        #         error_message = (
        #             'Header row does not follow the correct format'
        #         )
        #         upload_session.progress = error_message
        #         upload_session.error_file = (
        #             upload_session.process_file
        #         )
        #         upload_session.processed = True
        #         upload_session.save()
        #         return Response(
        #             {"status": "Header row does not follow the correct format"},
        #             status.HTTP_424_FAILED_DEPENDENCY
        #         )

        # finished = True
        # if finished:
        task = boundary_files_search.delay(1)

            # upload_session.token = task.id
            # upload_session.save()

        return Response({"status": "success"},
                            status.HTTP_201_CREATED)
