import json
import uuid
from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from core.settings.utils import absolute_path
from frontend.models.parcels import (
    Erf,
    Holding
)
from frontend.tests.model_factories import UserF
from frontend.tests.model_factories import BoundaryFileF
from frontend.models.boundary_search import (
    BoundarySearchRequest,
    SHAPEFILE
)
from frontend.utils.upload_file import (
    search_parcels_by_boundary_files
)


class TestUploadFileUtils(TestCase):

    def setUp(self) -> None:
        self.user_1 = UserF.create(username='test_1')
        # insert geom 1 and 2
        geom_path = absolute_path(
            'frontend', 'tests',
            'geojson', 'geom_1.geojson')
        with open(geom_path) as geojson:
            data = json.load(geojson)
            geom_str = json.dumps(data['features'][1]['geometry'])
            self.erf_1 = Erf.objects.create(
                geom=GEOSGeometry(geom_str),
                cname='C1234ABC'
            )
            geom_str = json.dumps(data['features'][0]['geometry'])
            self.holding_1 = Holding.objects.create(
                geom=GEOSGeometry(geom_str),
                cname='C1235DEF'
            )

    def test_search_parcels(self):
        session = str(uuid.uuid4())
        shapefile_path = absolute_path(
            'frontend', 'tests',
            'shapefile', 'test_within.zip')
        with open(shapefile_path, 'rb') as infile:
            _file = SimpleUploadedFile('test_within.zip', infile.read())
            BoundaryFileF.create(
                session=session,
                file_type='SHAPEFILE',
                file=_file,
                uploader=self.user_1
            )
        search_request = BoundarySearchRequest.objects.create(
            type='File',
            session=session,
            request_by=self.user_1
        )
        search_parcels_by_boundary_files(search_request)
        search_request = BoundarySearchRequest.objects.get(
            id=search_request.id
        )
        self.assertEqual(len(search_request.parcels), 1)
