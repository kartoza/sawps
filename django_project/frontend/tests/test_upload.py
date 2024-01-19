import uuid
import mock
from django.test import TestCase
from django.contrib.gis.geos import GEOSGeometry
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from core.settings.utils import absolute_path
from rest_framework.test import APIRequestFactory
from frontend.tests.model_factories import UserF
from frontend.models.base_task import DONE
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
    BoundaryFileSearchStatus,
    BoundaryFileGeoJson
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
        self.assertEqual(response.status_code, 204)
        self.assertTrue(BoundaryFile.objects.filter(
            name='admin.geojson',
            meta_id='layer-id',
            session=session
        ).exists())
        file = SimpleUploadedFile(
            'admin.kml',
            b'file_content',
            content_type='application/vnd.google-earth.kml+xml')
        session = str(uuid.uuid4())
        request = self.factory.post(
            reverse('boundary-file-upload'), {
                'session': session,
                'meta_id': 'layer-id',
                'file': file
            }
        )
        request.user = UserF.create()
        response = view(request)
        self.assertEqual(response.status_code, 204)
        self.assertTrue(BoundaryFile.objects.filter(
            name='admin.kml',
            meta_id='layer-id',
            session=session
        ).exists())
        shapefile_path = absolute_path(
            'frontend', 'tests',
            'shapefile', 'shapefile_1.zip')
        with open(shapefile_path, 'rb') as infile:
            file = SimpleUploadedFile(
                'shapefile_1.zip',
                infile.read(),
                content_type='application/zip')
            session = str(uuid.uuid4())
            request = self.factory.post(
                reverse('boundary-file-upload'), {
                    'session': session,
                    'meta_id': 'layer-id2',
                    'file': file
                }
            )
            request.user = UserF.create()
            response = view(request)
        self.assertEqual(response.status_code, 204)
        self.assertTrue(BoundaryFile.objects.filter(
            name='shapefile_1.zip',
            meta_id='layer-id2',
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
        search_request = BoundarySearchRequest.objects.filter(
            session=kwargs['session']
        ).first()
        self.assertTrue(search_request)
        self.assertEqual(search_request.type, 'File')
        # add using search_type
        kwargs = {
            'session': str(uuid.uuid4())
        }
        request = self.factory.get(
            reverse(
                'boundary-file-search',
                kwargs=kwargs
            ) + '?search_type=Digitise'
        )
        request.user = self.user_1
        view = BoundaryFileSearch.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 204)
        search_request = BoundarySearchRequest.objects.filter(
            session=kwargs['session']
        ).first()
        self.assertTrue(search_request)
        self.assertEqual(search_request.type, 'Digitise')

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
        self.assertIn('progress', response.data)

    def test_file_search_geojson(self):
        search_request = BoundarySearchRequest.objects.create(
            type='File',
            session=str(uuid.uuid4()),
            request_by=self.user_1,
        )
        kwargs = {
            'session': search_request.session
        }
        request = self.factory.get(
            reverse('boundary-file-geojson', kwargs=kwargs)
        )
        request.user = self.user_1
        view = BoundaryFileGeoJson.as_view()
        # unfinished task
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 404)
        search_request.status = DONE
        search_request.save()
        # empty geometry
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 404)
        search_request.geometry = GEOSGeometry("MULTIPOLYGON(((0 0, 0 1, 1 1, 1 0, 0 0)), ((2 2, 2 3, 3 3, 3 2, 2 2)))", srid=4326)
        search_request.save()
        # has geometry
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn('geometry', response.data)
