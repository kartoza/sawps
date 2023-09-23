import codecs
import csv
import logging
import pandas as pd
from datetime import datetime

from frontend.models import UploadSpeciesCSV
from property.models import Property
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from species.scripts.upload_file_scripts import COMPULSORY_FIELDS, SHEET_TITLE
from species.tasks.upload_species import upload_species_data

from species.scripts.data_upload import SpeciesCSVUpload

logger = logging.getLogger('sawps')


class SpeciesUploader(APIView):
    """API to upload csv file."""
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def check_header(self, headers):
        for header in COMPULSORY_FIELDS:
            if header not in headers:
                error_message = "The '{}' field is missing. Please check " \
                                "that all the compulsory fields are in the " \
                                "CSV file headers.".format(header)
                return error_message
        return

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

        if species_file.name.endswith('.xlsx'):
            xl = pd.ExcelFile(species_file)
            try:
                dataset = xl.parse(SHEET_TITLE)
                headers = dataset.columns.ravel()
            except ValueError:
                error = "The sheet named {} is not in the Excel " \
                             "file. Please download the template to get " \
                             "the correct file. ".format(SHEET_TITLE)
            else:
                error = self.check_header(headers)

        else:
            reader = csv.DictReader(codecs.iterdecode(species_file, 'utf-8'))
            headers = reader.fieldnames
            error = self.check_header(headers)

        if error:
            upload_session.error_notes = error
            upload_session.error_file = species_file
            upload_session.canceled = True
            upload_session.save()
            return Response(
                status=400,
                data={'detail': error}
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

        encoding = 'utf-8-sig'

        upload_session.progress = 'Processing'
        upload_session.save()
        file_upload = SpeciesCSVUpload()
        file_upload.upload_session = upload_session
        file_upload.start(encoding)

        # task = upload_species_data.delay(
        #     upload_session.id
        # )
        #
        # if task:
        #     return Response(
        #         status=200
        #     )
        #
        # return Response(
        #     status=404,
        #     data={
        #         'detail': 'Somthing wrong with the csv file'
        #     }
        # )


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
                    'property': (property_message if property_message
                                 else None),
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
