import uuid
import mock
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIRequestFactory
from core.settings.utils import absolute_path
from frontend.models.parcels import (
    Erf,
    Holding
)
from frontend.tests.model_factories import UserF
from frontend.models.boundary_search import (
    BoundaryFile,
    BoundarySearchRequest,
    SHAPEFILE
)
from frontend.api_views.upload import (
    BoundaryFileUpload,
    BoundaryFileRemove,
    BoundaryFileList,
    BoundaryFileSearch,
    BoundaryFileSearchStatus
)
from frontend.tests.model_factories import BoundaryFileF


class DummyTask:
    def __init__(self, id):
        self.id = id


def mocked_process(*args, **kwargs):
    return DummyTask('1')


class TestUploadAPIViews(TestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user_1 = UserF.create(username='test_1')

    @mock.patch(
        'frontend.api_views.upload.get_uploaded_file_crs',
        mock.Mock(return_value=('EPSG:4326')))
    def test_file_upload(self):
        file = SimpleUploadedFile(
            'admin.geojson',
            b'file_content',
            content_type='application/geo+json')
        session = str(uuid.uuid4())
        request = self.factory.post(
            reverse('boundary-file-upload'), {
                'session': session,
                'meta_id': 'layer-id',
                'file': file
            }
        )
        request.user = UserF.create()
        view = BoundaryFileUpload.as_view()
        response = view(request)
        print(response.data)
        self.assertEqual(response.status_code, 204)
        self.assertTrue(BoundaryFile.objects.filter(
            name='admin.geojson',
            meta_id='layer-id',
            session=session
        ).exists())

    def test_file_remove(self):
        # create obj
        file = BoundaryFileF.create(
            uploader=self.user_1,
            file_type=SHAPEFILE
        )
        data = {
            'session': file.session,
            'meta_id': file.meta_id
        }
        request = self.factory.post(
            reverse('boundary-file-remove'), data=data,
            format='json'
        )
        request.user = self.user_1
        view = BoundaryFileRemove.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_file_list(self):
        kwargs = {
            'session': str(uuid.uuid4())
        }
        request = self.factory.get(
            reverse('boundary-file-list', kwargs=kwargs)
        )
        request.user = self.user_1
        view = BoundaryFileList.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    @mock.patch(
        'frontend.api_views.upload.boundary_files_search.delay',
        mock.Mock(side_effect=mocked_process))
    def test_file_search(self):
        kwargs = {
            'session': str(uuid.uuid4())
        }
        request = self.factory.get(
            reverse('boundary-file-search', kwargs=kwargs)
        )
        request.user = self.user_1
        view = BoundaryFileSearch.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 204)

    def test_file_search_status(self):
        search_request = BoundarySearchRequest.objects.create(
            type='File',
            session=str(uuid.uuid4()),
            request_by=self.user_1,
        )
        kwargs = {
            'session': search_request.session
        }
        request = self.factory.get(
            reverse('boundary-file-status', kwargs=kwargs)
        )
        request.user = self.user_1
        view = BoundaryFileSearchStatus.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'PENDING')
