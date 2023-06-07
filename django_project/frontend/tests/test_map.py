from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from frontend.tests.model_factories import UserF
from frontend.api_views.map import (
    ContextLayerList,
    MapStyles
)


class TestMapAPIViews(TestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user_1 = UserF.create(username='test_1')
    
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

