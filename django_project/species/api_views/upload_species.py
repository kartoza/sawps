import codecs
import csv
from datetime import datetime

from frontend.models import UploadSpeciesCSV
from property.models import Property
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from scripts.csv_headers import CSV_FILE_HEADERS
from species.tasks.upload_species import upload_species_data


class SpeciesUploader(APIView):
    """API to upload csv file."""
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        species_file = request.FILES['file']

        if not species_file:
            return Response(
                status=400,
                data={
                    'detail': 'File not found'
                }
            )

        upload_session = UploadSpeciesCSV.objects.create(
            uploader=self.request.user,
            uploaded_at=datetime.now(),
            token=request.POST['token'],
            property=Property.objects.get(id=request.POST['property'])
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
                    status=400,
                    data={
                        'detail': 'Header row does not follow the '
                                  'correct format.' + header
                    }
                )
        upload_session.process_file = species_file
        upload_session.save()
        return Response(status=204)


class SaveCsvSpecies(APIView):
    """API to save csv file into the database."""
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            upload_session = UploadSpeciesCSV.objects.get(
                property=request.data.get('property'),
                uploader=self.request.user,
                token=request.data.get('token')
            )
        except UploadSpeciesCSV.DoesNotExist:
            return Response(
                status=400,
                data={
                    'detail': 'There is something wrong please try again.'
                }
            )
        task = upload_species_data.delay(
            upload_session.id
        )

        if task:
            return Response(
                status=200
            )

        return Response(
            status=404,
            data={
                'detail': 'Somthing wrong with the csv file'
            }
        )


class UploadSpeciesStatus(APIView):
    """Check upload species status."""
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        token = kwargs.get('token')
        try:
            upload_species = UploadSpeciesCSV.objects.get(
                token=token
            )
        except UploadSpeciesCSV.DoesNotExist:
            return Response(status=404)

        property_message = None
        taxon_message = None
        if upload_species.error_notes:
            messages = upload_species.error_notes.splitlines()
            property_message = messages[0]
            taxon_message = messages[1]

        if upload_species.canceled or not upload_species.processed:
            return Response(
                status=200,
                data={
                    'status': 'Canceled',
                    'property': (property_message if property_message else None),
                    'taxon': (taxon_message if taxon_message else None)
                }
            )

        return Response(
            status=200,
            data={
                'status': 'Done',
                'message': upload_species.success_notes,
                'property': (property_message if property_message else None),
                'taxon': (taxon_message if taxon_message else None)
            }
        )
