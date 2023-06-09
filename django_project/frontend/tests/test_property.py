import json
from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from core.settings.utils import absolute_path
from frontend.models.parcels import (
    Erf,
    Holding
)
from frontend.tests.model_factories import UserF
from frontend.api_views.property import CreateNewProperty


class TestPropertyAPIViews(TestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
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
    
    def test_create_new_property(self):
        data = {
            'name': 'Property A',
            'ownerEmail': 'test@test.com',
            'propertyTypeId': 1,
            'provinceId': 1,
            'organisationId': 1,
            'parcels': [
                {
                    'id': self.erf_1.id,
                    'layer': 'erf',
                    'cname': self.erf_1.cname,
                    'type': 'urban'
                },
                {
                    'id': self.holding_1.id,
                    'layer': 'holding',
                    'cname': self.holding_1.cname,
                    'type': 'urban'
                },
            ]
        }
        request = self.factory.post(
            reverse('property-create'), data=data,
            format='json'
        )
        request.user = self.user_1
        view = CreateNewProperty.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)

