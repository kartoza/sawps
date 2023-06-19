import json
from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from core.settings.utils import absolute_path
from property.factories import PropertyFactory
from stakeholder.factories import organisationUserFactory
from frontend.models.parcels import (
    Erf,
    Holding
)
from frontend.tests.model_factories import UserF
from frontend.api_views.map import (
    ContextLayerList,
    MapStyles,
    PropertiesLayerMVTTiles,
    FindParcelByCoord,
    FindPropertyByCoord
)


class TestMapAPIViews(TestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user_1 = UserF.create(username='test_1')
        self.superuser = UserF.create(
            username='test_2',
            is_superuser=True
        )
        self.user_2 = UserF.create(username='test_3')
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

    def test_get_properties_map_tile(self):
        kwargs = {
            'z': 14,
            'x': 9455,
            'y': 9454
        }
        request = self.factory.get(
            reverse('properties-map-layer', kwargs=kwargs)
        )
        request.user = self.user_1
        view = PropertiesLayerMVTTiles.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        # test superuser
        request = self.factory.get(
            reverse('properties-map-layer', kwargs=kwargs)
        )
        request.user = self.superuser
        view = PropertiesLayerMVTTiles.as_view()
        response = view(request, **kwargs)
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

    def test_find_property_by_coord(self):
        # insert property
        property = PropertyFactory.create(
            geometry=self.holding_1.geom,
            name='Property A',
            created_by=self.user_1
        )
        lat = -26.71998940486352
        lng = 27.763781680455708
        request = self.factory.get(
            reverse('find-property') + (
                f'/?lat={lat}&lng={lng}'
            )
        )
        # should find 1
        request.user = self.user_1
        view = FindPropertyByCoord.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], property.name)
        # user 2 should have no access
        request.user = self.user_2
        response = view(request)
        self.assertEqual(response.status_code, 404)
        # add user 2 to the organisation, should have access
        organisationUserFactory.create(
            organisation=property.organisation,
            user=self.user_2
        )
        request.user = self.user_2
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], property.name)
