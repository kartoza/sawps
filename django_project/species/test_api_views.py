from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from species.tasks.upload_species import (
    string_to_boolean,
    string_to_number
)


class TestUploadSpeciesApiView(TestCase):
    """Test api view species uploader"""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user',
            password='testpasswordt5D@/'
        )
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

        self.client.login(username=self.user.username, password='testpasswordt5D@/')

        response = self.client.post(
            self.api_url,
            request
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


    def test_task_string_to_boolean(self):
        """Test string_to_boolean functionality in task"""

        self.assertTrue(string_to_boolean('yes'))
        self.assertFalse(string_to_boolean(''))

    def test_task_string_to_number(self):
        """Test string_to_number functionality in task"""

        self.assertEqual(10, string_to_number('10'))
        self.assertEqual(0.0, string_to_number(''))
