from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status
from django.test import TestCase
from frontend.tests.model_factories import UploadSpeciesCSVF
from sawps.tests.models.account_factory import UserF
from django.core.files.uploadedfile import SimpleUploadedFile


class TestUploadSpeciesApiView(TestCase):
    """Test all api view"""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = UserF.create(is_superuser=True)
        self.api_url = '/api/upload-species/'

    def test_upload_species_without_login(self):
        """Test upload species api"""

        response = self.client.get(self.api_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_upload_session_with_invalid_file(self):
        """Test upload species api"""

        csv_file = SimpleUploadedFile(
            'file.csv', b'file_content',
            content_type='text/csv')

        request = {'file': csv_file}

        self.client.login(username=self.user.username, password='password')

        response = self.client.post(
            self.api_url,
            request
        )

        self.assertEqual(response.data, status.HTTP_424_FAILED_DEPENDENCY)
