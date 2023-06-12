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
from frontend.api_views.map import (
    ContextLayerList,
    MapStyles,
    FindParcelByCoord
)


class TestMapAPIViews(TestCase):

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

    def test_get_context_layers(self):
        request = self.factory.get(
            reverse('context-layer-list')
        )
        request.user = self.user_1
        view = ContextLayerList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_get_map_styles(self):
        request = self.factory.get(
            reverse('map-style')
        )
        request.user = self.user_1
        view = MapStyles.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_find_parcel_by_coord(self):
        lat = -26.71998940486352
        lng = 27.763781680455708
        request = self.factory.get(
            reverse('find-parcel') + (
                f'/?lat={lat}&lng={lng}'
            )
        )
        request.user = self.user_1
        view = FindParcelByCoord.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['layer'], 'holding')
        self.assertEqual(response.data['cname'], self.holding_1.cname)
