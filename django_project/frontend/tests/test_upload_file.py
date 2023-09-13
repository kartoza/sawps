import json
import uuid
import fiona
from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from core.settings.utils import absolute_path
from property.factories import ParcelFactory
from frontend.models.parcels import (
    Holding
)
from frontend.tests.model_factories import UserF
from frontend.tests.model_factories import BoundaryFileF
from frontend.models.boundary_search import (
    BoundarySearchRequest
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
            'geojson', 'parcel_1.geojson')
        with fiona.open(geom_path, encoding='utf-8') as layer:
            # 1 feature only
            for feature in layer:
                geom_str = json.dumps(feature['geometry'])
                # geom_str without crs info is assumed to be in 4326
                geom = GEOSGeometry(GEOSGeometry(geom_str).wkt, srid=3857)
                self.holding_1 = Holding.objects.create(
                    geom=geom,
                    cname='C1235DEF'
                )
                break

    def test_search_parcels(self):
        session = str(uuid.uuid4())
        shapefile_path = absolute_path(
            'frontend', 'tests',
            'shapefile', 'shapefile_1.zip')
        with open(shapefile_path, 'rb') as infile:
            _file = SimpleUploadedFile('shapefile_1.zip', infile.read())
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
        self.assertEqual(len(search_request.used_parcels), 0)
        # add parcel property with holding_1
        ParcelFactory.create(
            sg_number=self.holding_1.cname
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
        self.assertEqual(len(search_request.parcels), 0)
        self.assertEqual(len(search_request.used_parcels), 1)
        
