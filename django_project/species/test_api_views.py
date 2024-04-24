import csv
from unittest import mock
import pandas as pd
from activity.models import ActivityType
from core.settings.utils import absolute_path
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError
from frontend.models.upload import UploadSpeciesCSV
from frontend.tests.model_factories import UserF
from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity,
    OpenCloseSystem,
    PopulationStatus,
    SamplingEffortCoverage,
    PopulationEstimateCategory
)
from property.models import Property
from property.factories import PropertyFactory
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory
from species.api_views.upload_species import (
    SaveCsvSpecies,
    SpeciesUploader,
    UploadSpeciesStatus,
)
from species.models import Taxon
from species.tasks.upload_species import (
    upload_species_data,
    try_delete_uploaded_file
)
from species.scripts.data_upload import (
    SpeciesCSVUpload,
    string_to_boolean,
    string_to_number,
    map_string_to_value
)
from species.scripts.upload_file_scripts import *  # noqa
from stakeholder.factories import (
    organisationRepresentativeFactory,
    organisationUserFactory
)
from population_data.factories import AnnualPopulationF
from occurrence.models import SurveyMethod


def mocked_run_func(encoding):
    pass


class TestUploadSpeciesApiView(TestCase):
    """Test api view species uploader"""
    fixtures = [
        'activity_type.json',
        'open_close_systems.json',
        'population_status.json',
        'sampling_effort_coverage.json',
        'survey_methods',
        'population_estimate_category.json'
    ]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = UserF(is_superuser=True)
        self.property = PropertyFactory(
            name="Luna"
        )
        # not belong to any organisation
        self.non_superuser_1 = UserF()
        # as manager
        self.non_superuser_2 = UserF()
        organisationRepresentativeFactory.create(
            organisation=self.property.organisation,
            user=self.non_superuser_2
        )
        # as member
        self.non_superuser_3 = UserF()
        organisationUserFactory.create(
            organisation=self.property.organisation,
            user=self.non_superuser_3
        )
        Property.objects.filter(id=self.property.id).update(
            short_code='Luna'
        )
        self.property.refresh_from_db()
        self.token = '8f1c1181-982a-4286-b2fe-da1abe8f7174'
        self.api_url = '/api/upload-species/'
        self.lion = Taxon.objects.create(
            scientific_name='Panthera leo',
            common_name_verbatim='Lion'
        )

    def test_upload_species_without_login(self):
        """Test upload species api"""

        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_upload_session_incorrect(self):
        """Test upload species with incorrect header"""

        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'incorrect.csv')
        data = open(csv_path, 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        request = self.factory.post(
            reverse('upload-species'), {
                'file': data,
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(UploadSpeciesCSV.objects.filter(token=self.token).count(),
                         1)
        upload_session = UploadSpeciesCSV.objects.get(token=self.token)
        self.assertTrue(upload_session.canceled)
        self.assertEqual(upload_session.process_file.name, '')
        self.assertEqual(upload_session.error_notes,
                         "The 'Property_code' field is missing. "
                         "Please check that all the compulsory fields "
                         "are in the CSV file headers."
                         )

    def test_upload_session_no_sheet(self):
        """Test upload species with no sheet in excel file."""

        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'excel_no_sheet.xlsx')
        data = open(csv_path, 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        request = self.factory.post(
            reverse('upload-species'), {
                'file': data,
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(UploadSpeciesCSV.objects.filter(token=self.token).count(),
                         1)
        upload_session = UploadSpeciesCSV.objects.get(token=self.token)
        self.assertTrue(upload_session.canceled)
        self.assertEqual(upload_session.process_file.name, '')
        self.assertEqual(upload_session.error_notes,
                         "The sheet named Dataset pilot is not in the Excel "
                         "file. Please download the template to get "
                         "the correct file."
                         )

    def test_save_csv_with_no_property(self):
        """Test save csv with not existing property."""

        request = self.factory.post(
            reverse('save-csv-species'),
            data={
                'token': self.token,
                'property': 0
            }, format='json')

        request.user = self.user
        view = SaveCsvSpecies.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_upload_session(self):
        """Test upload species """

        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'test.csv')
        data = open(csv_path, 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        request = self.factory.post(
            reverse('upload-species'), {
                'file': data,
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(UploadSpeciesCSV.objects.filter(token=self.token).count(),
                         1)
        file_name = 'species'
        upload_session = UploadSpeciesCSV.objects.get(token=self.token)
        self.assertTrue(file_name in upload_session.process_file.path)
        self.assertEqual(upload_session.error_file.name, '')

        with mock.patch('species.api_views.upload_species.upload_species_data.delay') as mock_task:
            request = self.factory.post(
                reverse('save-csv-species'),
                data={
                    'token': self.token,
                    'property': self.property.id
                }, format='json')

            request.user = self.user
            view = SaveCsvSpecies.as_view()
            response = view(request)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(mock_task.called)

    @mock.patch("species.tasks.upload_species.upload_species_data")
    def test_upload_csv_task(self, mock_app):
        """Test upload csv task."""
        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'test.csv')
        data = open(csv_path, 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        request = self.factory.post(
            reverse('upload-species'), {
                'file': data,
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 204)
        upload_session = UploadSpeciesCSV.objects.get(token=self.token)

        upload_species_data(upload_session.id)
        self.assertEqual(Taxon.objects.all().count(), 1)
        self.assertEqual(AnnualPopulationPerActivity.objects.all().count(), 5)
        self.assertEqual(AnnualPopulation.objects.all().count(), 1)
        population_data = AnnualPopulation.objects.all().first()
        self.assertEqual(population_data.total, 190)
        self.assertEqual(population_data.adult_total, 150)
        self.assertTrue(AnnualPopulationPerActivity.objects.filter(
            activity_type__name="Translocation (Offtake)"
        ).count(), 1)
        self.assertTrue(AnnualPopulationPerActivity.objects.filter(
            activity_type__name="Planned Hunt/Cull"
        ).count(), 1)
        self.assertTrue(AnnualPopulationPerActivity.objects.filter(
            activity_type__name="Translocation (Intake)"
        ).count(), 1)
        self.assertTrue(AnnualPopulationPerActivity.objects.filter(
            activity_type__name="Planned Euthanasia/DCA"
        ).count(), 1)
        self.assertTrue(AnnualPopulationPerActivity.objects.filter(
            activity_type__name="Unplanned/Illegal Hunting"
        ).count(), 1)
        self.assertTrue(AnnualPopulationPerActivity.objects.filter(
            translocation_destination="KNP", offtake_permit="ABC100X10"
        ).count(), 1)
        self.assertTrue(AnnualPopulationPerActivity.objects.filter(
            offtake_permit="DEF100X10"
        ).count(), 1)

        self.assertTrue(OpenCloseSystem.objects.all().count() == 3)

    def test_upload_species_status(self):
        """Test upload species status."""
        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'test.csv')
        data = open(csv_path, 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        request = self.factory.post(
            reverse('upload-species'), {
                'file': data,
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 204)
        upload_session = UploadSpeciesCSV.objects.get(token=self.token)

        upload_session.progress = 'Processing'
        upload_session.save()
        file_upload = SpeciesCSVUpload()
        file_upload.upload_session = upload_session
        file_upload.start('utf-8-sig')

        kwargs = {
            'token': self.token
        }
        request = self.factory.get(
            reverse('upload-species-status', kwargs=kwargs)
        )
        request.user = self.user
        view = UploadSpeciesStatus.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'Finished')
        self.assertFalse(response.data['error_file'])

    def test_upload_species_status_404(self):
        """Test upload species status with 404 error."""
        kwargs = {
            'token': '8f1c1181-982a-4286-b2fe-da1abe8f7172'
        }
        request = self.factory.get(
            reverse('upload-species-status', kwargs=kwargs)
        )
        request.user = self.user
        view = UploadSpeciesStatus.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 404)

    def test_upload_species_open_close_not_exist(self):
        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'test_open_close_not_exist.csv')
        data = open(csv_path, 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        request = self.factory.post(
            reverse('upload-species'), {
                'file': data,
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 204)
        upload_session = UploadSpeciesCSV.objects.get(token=self.token)
        upload_session.progress = 'Processing'
        upload_session.save()
        file_upload = SpeciesCSVUpload()
        file_upload.upload_session = upload_session
        file_upload.start('utf-8-sig')

        kwargs = {
            'token': self.token
        }
        request = self.factory.get(
            reverse('upload-species-status', kwargs=kwargs)
        )
        request.user = self.user
        view = UploadSpeciesStatus.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('media' in response.data['error_file'])

        self.assertTrue('error' in upload_session.error_file.path)
        with open(upload_session.error_file.path, encoding='utf-8-sig') as csv_file:
            error_file = csv.DictReader(csv_file)
            headers = error_file.fieldnames
            self.assertTrue('error_message' in headers)
            errors = []
            for row in error_file:
                errors.append(row['error_message'])
            self.assertTrue(
                "Open/Close system 'Close' does not exist" in errors
            )

    def test_upload_species_future_year(self):
        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'test_future_year.csv')
        data = open(csv_path, 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        request = self.factory.post(
            reverse('upload-species'), {
                'file': data,
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 204)
        upload_session = UploadSpeciesCSV.objects.get(token=self.token)
        upload_session.progress = 'Processing'
        upload_session.save()
        file_upload = SpeciesCSVUpload()
        file_upload.upload_session = upload_session
        file_upload.start('utf-8-sig')

        kwargs = {
            'token': self.token
        }
        request = self.factory.get(
            reverse('upload-species-status', kwargs=kwargs)
        )
        request.user = self.user
        view = UploadSpeciesStatus.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('media' in response.data['error_file'])

        self.assertTrue('error' in upload_session.error_file.path)
        with open(upload_session.error_file.path, encoding='utf-8-sig') as csv_file:
            error_file = csv.DictReader(csv_file)
            headers = error_file.fieldnames
            self.assertTrue('error_message' in headers)
            errors = []
            for row in error_file:
                errors.append(row['error_message'])
                print(errors)
            self.assertTrue(
                "'Year_of_estimate' with value 2080 exceeds current year."
                in errors
            )

    def test_upload_species_status_not_processed(self):
        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'test.csv')
        data = open(csv_path, 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        request = self.factory.post(
            reverse('upload-species'), {
                'file': data,
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 204)
        kwargs = {
            'token': self.token
        }
        request = self.factory.get(
            reverse('upload-species-status', kwargs=kwargs)
        )
        request.user = self.user
        view = UploadSpeciesStatus.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], False)


    def test_task_string_to_boolean(self):
        """Test string_to_boolean functionality in task"""

        self.assertTrue(string_to_boolean('yes'))
        self.assertFalse(string_to_boolean(''))

    def test_task_string_to_number(self):
        """Test string_to_number functionality in task"""

        self.assertEqual(10, string_to_number('10'))
        self.assertEqual(0.0, string_to_number(''))

    def test_upload_species_with_property_taxon_not_exist(self):
        """Test upload species task with a property and taxon not existing."""

        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'test_property_taxon.csv')
        data = open(csv_path, 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        request = self.factory.post(
            reverse('upload-species'), {
                'file': data,
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 204)
        upload_session = UploadSpeciesCSV.objects.get(token=self.token)
        upload_session.progress = 'Processing'
        upload_session.save()
        file_upload = SpeciesCSVUpload()
        file_upload.upload_session = upload_session
        file_upload.start('utf-8-sig')

        kwargs = {
            'token': self.token
        }
        request = self.factory.get(
            reverse('upload-species-status', kwargs=kwargs)
        )
        request.user = self.user
        view = UploadSpeciesStatus.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('media' in response.data['error_file'])

        self.assertTrue('error' in upload_session.error_file.path)
        with open(upload_session.error_file.path, encoding='utf-8-sig') as csv_file:
            error_file = csv.DictReader(csv_file)
            headers = error_file.fieldnames
            self.assertTrue('error_message' in headers)
            errors = []
            for row in error_file:
                errors.append(row['error_message'])
            self.assertTrue("Property code Luna's Reserve doesn't match "
                            "the selected property. Please replace "
                            "it with Luna." in errors)
            self.assertTrue("Lemurs doesn't exist in the database. "
                            "Please select species available in the "
                            "dropdown only." in errors)
            self.assertTrue("The value of field "
                            "If_other_(population_estimate_category)_please "
                            "explain is empty." in errors)
            self.assertTrue("The value of field "
                            "If_other_(survey_method)_please "
                            "explain is empty." in errors)
            self.assertTrue("The value of the compulsory field "
                            "Population_estimate_category is empty." in errors)
            self.assertTrue("The value of the compulsory field "
                            "presence/absence is empty. The value "
                            "of the compulsory field "
                            "Population_estimate_category is empty." in errors)
            self.assertTrue("The total of Count_adult_males and "
                            "Count_adult_females must not exceed "
                            "COUNT_TOTAL." in errors)

            # TODO: Check why this test is failing
            # self.assertTrue("The total of "
            #                 "Planned hunt/culling_Offtake_adult_males and "
            #                 "Planned hunt/culling_Offtake_adult_females must "
            #                 "not exceed Planned hunt/culling_TOTAL." in errors)
        self.assertEqual(AnnualPopulation.objects.count(), 7)
        self.assertEqual(upload_session.success_notes, "7 rows uploaded successfully.")
        self.assertTrue(AnnualPopulation.objects.filter(
            survey_method_other="Test survey"
        ).count(), 1)
        self.assertTrue(AnnualPopulation.objects.filter(
            survey_method__name="Other - please explain",
            survey_method_other="Test survey"
        ).count(), 1)
        self.assertTrue(AnnualPopulation.objects.filter(
            population_estimate_category__name="Other (please describe how the "
                                               "population size estimate was "
                                               "determined)",
            population_estimate_category_other="Decennial census"
        ).count(), 1)
        self.assertTrue(AnnualPopulation.objects.filter(
            population_estimate_category__name="Ad hoc or "
                                               "opportunistic monitoring"
        ).count(), 1)
        self.assertTrue(AnnualPopulationPerActivity.objects.filter(
            intake_permit="12345"
        ).count(), 1)
        self.assertTrue(AnnualPopulationPerActivity.objects.filter(
            reintroduction_source="KNP"
        ).count(), 1)
        self.assertTrue(AnnualPopulationPerActivity.objects.filter(
            founder_population=True
        ).count(), 1)

    def test_upload_excel_missing_compulsory_field(self):
        """Test upload species with an excel file which misses
         a compulsory field."""

        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'excel_wrong_header.xlsx')
        data = open(csv_path, 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        request = self.factory.post(
            reverse('upload-species'), {
                'file': data,
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(UploadSpeciesCSV.objects.filter(token=self.token).count(),
                         1)
        upload_session = UploadSpeciesCSV.objects.get(token=self.token)
        self.assertTrue(upload_session.canceled)
        self.assertEqual(upload_session.process_file.name, '')
        self.assertEqual(upload_session.error_notes,
                         "The 'Property_code' field is missing. Please check "
                         "that all the compulsory fields are in the "
                         "CSV file headers."
                         )

    def test_upload_species_with_excel_property_not_exist(self):
        """Test upload Excel file with a property not existing."""

        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'excel_error_property.xlsx')
        data = open(csv_path, 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        request = self.factory.post(
            reverse('upload-species'), {
                'file': data,
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 204)
        upload_session = UploadSpeciesCSV.objects.get(token=self.token)
        upload_session.progress = 'Processing'
        upload_session.save()
        file_upload = SpeciesCSVUpload()
        file_upload.upload_session = upload_session
        file_upload.start('utf-8-sig')
        self.assertTrue('error' in upload_session.error_file.path)

        xl = pd.ExcelFile(upload_session.error_file.path)
        dataset = xl.parse(SHEET_TITLE)
        self.assertEqual(
            dataset.iloc[0]['error_message'],
            "Property code Venetia Limpopo doesn't match the selected "
            "property. Please replace it with {}. Loxodonta africana "
            "doesn't exist in the database. Please select species "
            "available in the dropdown only.".format(
                upload_session.property.short_code
            )
        )
        # create two properties with code Venetia Limpopo
        # should return same error
        property1 = PropertyFactory(
            name="Venetia Limpopo"
        )
        property2 = PropertyFactory(
            name="Venetia Limpopo 2"
        )
        Property.objects.filter(id__in=[property1.id, property2.id]).update(
            short_code='Venetia Limpopo'
        )
        upload_session = UploadSpeciesCSV.objects.get(token=self.token)
        upload_session.progress = 'Processing'
        upload_session.save()
        file_upload = SpeciesCSVUpload()
        file_upload.upload_session = upload_session
        file_upload.start('utf-8-sig')
        self.assertTrue('error' in upload_session.error_file.path)

        xl = pd.ExcelFile(upload_session.error_file.path)
        dataset = xl.parse(SHEET_TITLE)
        self.assertEqual(
            dataset.iloc[0]['error_message'],
            "Property code Venetia Limpopo doesn't match the selected "
            "property. Please replace it with {}. Loxodonta africana "
            "doesn't exist in the database. Please select species "
            "available in the dropdown only.".format(
                upload_session.property.short_code
            )
        )

    @mock.patch("species.tasks.upload_species.upload_species_data")
    def test_upload_task_with_upload_session_not_existing(self, mock_app):
        """Test upload task with upload session not existing."""

        self.assertEqual(upload_species_data(1), None)

    def test_uploader_view_without_file(self):
        """Test uploader file view with no file"""

        request = self.factory.post(
            reverse('upload-species'), {
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'File not found')

    def test_uploader_view_with_empty_compulsory_fields(self):
        """Test uploader file view with an empty value in
        compulsory field."""

        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'test_empty_value_of_compulsory_fields.csv')
        data = open(csv_path, 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        request = self.factory.post(
            reverse('upload-species'), {
                'file': data,
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 204)
        upload_session = UploadSpeciesCSV.objects.get(token=self.token)
        upload_session.progress = 'Processing'
        upload_session.save()
        file_upload = SpeciesCSVUpload()
        file_upload.upload_session = upload_session
        file_upload.start('utf-8-sig')
        self.assertTrue('error' in upload_session.error_file.path)

    def test_upload_species_status_empty_file(self):
        """Test upload with empty file."""
        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'test_empty.csv')
        data = open(csv_path, 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        request = self.factory.post(
            reverse('upload-species'), {
                'file': data,
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 204)
        upload_session = UploadSpeciesCSV.objects.get(token=self.token)

        upload_session.progress = 'Processing'
        upload_session.save()
        file_upload = SpeciesCSVUpload()
        file_upload.upload_session = upload_session
        file_upload.start('utf-8-sig')

        kwargs = {
            'token': self.token
        }
        request = self.factory.get(
            reverse('upload-species-status', kwargs=kwargs)
        )
        request.user = self.user
        view = UploadSpeciesStatus.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'Error')
        self.assertFalse(response.data['error_file'])
        self.assertEqual(
            response.data['message'],
            'You have uploaded empty spreadsheet, please check again.'
        )
        upload_session.refresh_from_db()
        self.assertEqual(
            upload_session.error_notes,
            'You have uploaded empty spreadsheet, please check again.'
        )

    def test_upload_excel_invalid_area_available(self):
        """Test upload species with a csv file that has invalid
        area available to species."""

        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'test_invalid_area_available.csv')
        data = open(csv_path, 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        request = self.factory.post(
            reverse('upload-species'), {
                'file': data,
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 204)
        upload_session = UploadSpeciesCSV.objects.get(token=self.token)
        upload_session.progress = 'Processing'
        upload_session.save()
        file_upload = SpeciesCSVUpload()
        file_upload.upload_session = upload_session
        file_upload.start('utf-8-sig')
        upload_session.refresh_from_db()
        self.assertTrue('error' in upload_session.error_file.path)
        with open(upload_session.error_file.path, encoding='utf-8-sig') as csv_file:
            error_file = csv.DictReader(csv_file)
            headers = error_file.fieldnames
            self.assertTrue('error_message' in headers)
            errors = []
            for row in error_file:
                errors.append(row['error_message'])
            self.assertTrue(
                "Area available to species must be greater than 0 "
                "and less than or equal to property area size ({:.2f} ha).".format(
                    self.property.property_size_ha) in errors)

    def test_try_delete_uploaded_file(self):
        upload_session = UploadSpeciesCSV.objects.create(
            property=self.property,
            uploader=self.user
        )
        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'test.csv')
        with open(csv_path, 'rb') as data:
            upload_session.updated_file.save('test.csv', File(data))
            upload_session.error_file.save('test_error.csv', File(data))
        self.assertTrue(upload_session.updated_file)
        self.assertTrue(upload_session.error_file)
        try_delete_uploaded_file(upload_session.updated_file)
        self.assertFalse(upload_session.updated_file)
        with mock.patch('species.tasks.upload_species.FieldFile.delete',
                        side_effect=Exception("ERROR")) as mocked_delete:
            try_delete_uploaded_file(upload_session.error_file)
            mocked_delete.assert_called_once()
        self.assertTrue(upload_session.error_file)

    def test_rerun_upload(self):
        upload_session = UploadSpeciesCSV.objects.create(
            property=self.property,
            uploader=self.user
        )
        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'test.csv')
        with open(csv_path, 'rb') as data:
            upload_session.success_file.save('test.csv', File(data))
            upload_session.error_file.save('test_error.csv', File(data))
        self.assertTrue(upload_session.success_file)
        self.assertTrue(upload_session.error_file)
        with mock.patch('species.tasks.upload_species.SpeciesCSVUpload.start',
                        side_effect=mocked_run_func) as mocked_run:
            upload_species_data(upload_session.id)
            mocked_run.assert_called_once()
        upload_session.refresh_from_db()
        self.assertFalse(upload_session.success_file)
        self.assertFalse(upload_session.error_file)
        self.assertFalse(upload_session.canceled)

    def test_overwrite_annual_population(self):
        """Test upload species multiple times to overwrite data."""
        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'test_first_upload.csv')
        data = open(csv_path, 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        request = self.factory.post(
            reverse('upload-species'), {
                'file': data,
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 204)
        upload_session = UploadSpeciesCSV.objects.get(token=self.token)
        upload_session.progress = 'Processing'
        upload_session.save()
        file_upload = SpeciesCSVUpload()
        file_upload.upload_session = upload_session
        file_upload.start('utf-8-sig')

        kwargs = {
            'token': self.token
        }
        request = self.factory.get(
            reverse('upload-species-status', kwargs=kwargs)
        )
        request.user = self.user
        view = UploadSpeciesStatus.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'Finished')
        self.assertEqual(AnnualPopulation.objects.count(), 3)
        self.assertEqual(upload_session.success_notes, "3 rows uploaded successfully.")
        annual_2010 = AnnualPopulation.objects.filter(
            property=self.property,
            taxon=self.lion,
            year=2010
        ).first()
        self.assertTrue(annual_2010)
        self.assertEqual(annual_2010.total, 190)
        self.assertEqual(AnnualPopulationPerActivity.objects.filter(
            annual_population=annual_2010
        ).count(), 5)
        annual_2011 = AnnualPopulation.objects.filter(
            property=self.property,
            taxon=self.lion,
            year=2011
        ).first()
        self.assertTrue(annual_2011)
        self.assertEqual(annual_2011.total, 190)
        self.assertEqual(AnnualPopulationPerActivity.objects.filter(
            annual_population=annual_2011
        ).count(), 5)
        annual_2012 = AnnualPopulation.objects.filter(
            property=self.property,
            taxon=self.lion,
            year=2012
        ).first()
        self.assertTrue(annual_2012)
        self.assertEqual(annual_2012.total, 190)
        self.assertEqual(AnnualPopulationPerActivity.objects.filter(
            annual_population=annual_2012
        ).count(), 4)
        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'test_second_upload.csv')
        data = open(csv_path, 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        request = self.factory.post(
            reverse('upload-species'), {
                'file': data,
                'token': self.token,
                'property': self.property.id
            }
        )
        request.user = self.user
        view = SpeciesUploader.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 204)
        upload_session = UploadSpeciesCSV.objects.get(token=self.token)
        upload_session.progress = 'Processing'
        upload_session.save()
        file_upload = SpeciesCSVUpload()
        file_upload.upload_session = upload_session
        file_upload.start('utf-8-sig')

        kwargs = {
            'token': self.token
        }
        request = self.factory.get(
            reverse('upload-species-status', kwargs=kwargs)
        )
        request.user = self.user
        view = UploadSpeciesStatus.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'Finished')
        self.assertEqual(AnnualPopulation.objects.count(), 3)
        self.assertEqual(upload_session.success_notes,
                         "2 rows already exist and have been overwritten.")
        annual_2010.refresh_from_db()
        annual_2011.refresh_from_db()
        annual_2012.refresh_from_db()
        # ensure no change for 2010
        self.assertEqual(annual_2010.total, 190)
        self.assertEqual(AnnualPopulationPerActivity.objects.filter(
            annual_population=annual_2010
        ).count(), 5)
        self.assertEqual(annual_2011.total, 240)
        self.assertEqual(AnnualPopulationPerActivity.objects.filter(
            annual_population=annual_2011
        ).count(), 0)
        self.assertEqual(annual_2012.total, 160)
        self.assertEqual(AnnualPopulationPerActivity.objects.filter(
            annual_population=annual_2012
        ).count(), 1)
        self.assertTrue(AnnualPopulationPerActivity.objects.filter(
            annual_population=annual_2012,
            activity_type__name="Translocation (Offtake)",
            total=20
        ).exists())

    def test_upload_data_permission(self):
        # test upload with organisation member
        upload_session = UploadSpeciesCSV.objects.create(
            property=self.property,
            uploader=self.non_superuser_3
        )
        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'test.csv')
        with open(csv_path, 'rb') as data:
            upload_session.process_file.save('test.csv', File(data))
        upload_species_data(upload_session.id)
        upload_session.refresh_from_db()
        self.assertTrue(upload_session.success_notes)
        self.assertEqual(upload_session.success_notes, '1 rows uploaded successfully.')
        self.assertFalse(upload_session.error_file)
        AnnualPopulation.objects.filter(
            property=self.property,
            taxon=self.lion,
            year=2017
        ).delete()
        # test upload with organisation manager
        upload_session.uploader = self.non_superuser_2
        upload_session.save(update_fields=['uploader'])
        upload_species_data(upload_session.id)
        upload_session.refresh_from_db()
        self.assertTrue(upload_session.success_notes)
        self.assertEqual(upload_session.success_notes, '1 rows uploaded successfully.')
        self.assertFalse(upload_session.error_file)
        AnnualPopulation.objects.filter(
            property=self.property,
            taxon=self.lion,
            year=2017
        ).delete()
        # test upload with non-organisation member
        upload_session.uploader = self.non_superuser_1
        upload_session.save(update_fields=['uploader'])
        upload_species_data(upload_session.id)
        upload_session.refresh_from_db()
        self.assertFalse(upload_session.success_notes)
        self.assertTrue(upload_session.error_file)
        with open(upload_session.error_file.path, encoding='utf-8-sig') as csv_file:
            error_file = csv.DictReader(csv_file)
            headers = error_file.fieldnames
            self.assertTrue('error_message' in headers)
            errors = []
            for row in error_file:
                errors.append(row['error_message'])
            self.assertIn("You are not allowed to add data to property {}".format(
                    self.property.short_code), errors)

    def test_update_data_permission(self):
        upload_session = UploadSpeciesCSV.objects.create(
            property=self.property,
            uploader=self.non_superuser_3
        )
        csv_path = absolute_path(
            'frontend', 'tests',
            'csv', 'test.csv')
        with open(csv_path, 'rb') as data:
            upload_session.process_file.save('test.csv', File(data))
        upload_species_data(upload_session.id)
        upload_session.refresh_from_db()
        self.assertTrue(upload_session.success_notes)
        self.assertEqual(upload_session.success_notes, '1 rows uploaded successfully.')
        self.assertFalse(upload_session.error_file)
        # uploader can update the data
        upload_species_data(upload_session.id)
        upload_session.refresh_from_db()
        self.assertTrue(upload_session.success_notes)
        self.assertEqual(upload_session.success_notes, '1 rows already exist and have been overwritten.')
        self.assertFalse(upload_session.error_file)
        # test upload with organisation manager
        upload_session.uploader = self.non_superuser_2
        upload_session.save(update_fields=['uploader'])
        upload_species_data(upload_session.id)
        upload_session.refresh_from_db()
        self.assertTrue(upload_session.success_notes)
        self.assertEqual(upload_session.success_notes, '1 rows already exist and have been overwritten.')
        self.assertFalse(upload_session.error_file)
        # test upload with non-organisation member
        upload_session.uploader = self.non_superuser_1
        upload_session.save(update_fields=['uploader'])
        upload_species_data(upload_session.id)
        upload_session.refresh_from_db()
        self.assertFalse(upload_session.success_notes)
        self.assertTrue(upload_session.error_file)
        with open(upload_session.error_file.path, encoding='utf-8-sig') as csv_file:
            error_file = csv.DictReader(csv_file)
            headers = error_file.fieldnames
            self.assertTrue('error_message' in headers)
            errors = []
            for row in error_file:
                errors.append(row['error_message'])
            self.assertIn("You are not allowed to update data of property {} and species {} in year {}".format(
                    self.property.short_code, self.lion.scientific_name, 2017), errors)

    def test_map_string_to_value(self):
        dict_values = {
            'test': 'ABC'
        }
        self.assertEqual(
            map_string_to_value('test', dict_values),
            'ABC'
        )
        self.assertFalse(map_string_to_value('null', dict_values))

    def test_row_value_invalid_key(self):
        row = {
            'test': 'ABC'
        }
        file_upload = SpeciesCSVUpload()
        self.assertFalse(file_upload.row_value(row, 'null'))

    @mock.patch('population_data.models.AnnualPopulationPerActivity.objects.get_or_create')
    def test_save_population_per_activity(self, mocked_create):
        mocked_create.side_effect = IntegrityError('error')
        file_upload = SpeciesCSVUpload()
        annual = AnnualPopulationF.create(
            year=2023
        )
        row = {
            INTRODUCTION_TOTAL: '22',
            INTRODUCTION_TOTAL_MALES: '22',
            INTRODUCTION_TOTAL_FEMALES: '22',
            INTRODUCTION_MALE_JUV: '22',
            INTRODUCTION_FEMALE_JUV: '22'
        }
        intake = file_upload.save_population_per_activity(
            row, ACTIVITY_TRANSLOCATION_INTAKE, 2023,
            annual, INTRODUCTION_TOTAL,
            INTRODUCTION_TOTAL_MALES, INTRODUCTION_TOTAL_FEMALES,
            INTRODUCTION_MALE_JUV, INTRODUCTION_FEMALE_JUV
        )
        self.assertFalse(intake)
        self.assertEqual(len(file_upload.row_error), 1)
        # test with invalid activity type
        file_upload.row_error = []
        intake = file_upload.save_population_per_activity(
            row, 'invalid', 2023,
            annual, INTRODUCTION_TOTAL,
            INTRODUCTION_TOTAL_MALES, INTRODUCTION_TOTAL_FEMALES,
            INTRODUCTION_MALE_JUV, INTRODUCTION_FEMALE_JUV
        )
        self.assertFalse(intake)
        self.assertEqual(len(file_upload.row_error), 1)

    def test_invalid_dropdown_values(self):
        file_upload = SpeciesCSVUpload()
        row = {
            SAMPLING_EFFORT: '',
            SURVEY_METHOD: 'invalid',
            PRESENCE: 'invalid',
            OPEN_SYS: ''
        }
        self.assertFalse(file_upload.sampling_effort(row))
        self.assertFalse(file_upload.survey_method(row))
        self.assertFalse(file_upload.presence(row))
        self.assertFalse(file_upload.open_close_system(row))
        self.assertEqual(len(file_upload.row_error), 2)
