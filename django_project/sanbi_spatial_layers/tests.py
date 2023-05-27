from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from sanbi_spatial_layers.models import WMS
from django.forms.models import model_to_dict


class TestWMSRestViews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staffuser = User.objects.create_user(
            username='test_staff_user', password='Test1234', is_staff=True
        )
        cls.user = User.objects.create_user(
            username='test_user', password='Test1234'
        )

    def tearDown(self):
        super().tearDown()
        self.client.logout()

    def test_create_wms_layer_staff_user(self):
        """create wms layer with staff user"""
        self.client.login(username='test_staff_user', password='Test1234')
        wms = {
            'name': 'wms layer - test',
            'type': 'WMS layer',
            'description': 'testing wms creation',
            'url': 'http://ows.mundialis.de/services/service?',
        }
        response = self.client.post(reverse('add_wms_layer'), wms)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        wms_layer = WMS.objects.all()[0]
        self.assertEqual(wms_layer.name, 'wms layer - test')

    def test_create_wms_layer_non_staff_user(self):
        """fails to create wms layer with a non-staff user"""
        self.client.login(username='test_user', password='Test1234')
        wms = {
            'name': 'wms layer - test',
            'type': 'WMS layer',
            'description': 'testing wms creation',
            'url': 'http://ows.mundialis.de/services/service?',
        }
        response = self.client.post(reverse('add_wms_layer'), wms)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_wms_layer_anonymous_user(self):
        """fails to create wms layer when there is an anonymous user"""
        wms = {
            'name': 'wms layer - test',
            'type': 'WMS layer',
            'description': 'testing wms creation',
            'url': 'http://ows.mundialis.de/services/service?',
        }
        response = self.client.post(reverse('add_wms_layer'), wms)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_wms_layers(self):
        """list wms layers"""
        self.client.login(username='test_staff_user', password='Test1234')
        wms = {
            'id': '1',
            'name': 'wms layer - test',
            'type': 'WMS layer',
            'description': 'testing wms creation',
            'url': 'http://ows.mundialis.de/services/service?',
        }
        self.client.post(reverse('add_wms_layer'), wms)
        response = self.client.get(reverse('list_wms_layers'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_wms_layers(self):
        """get a layer using <int:id>"""
        self.client.login(username='test_staff_user', password='Test1234')
        wms = {
            'name': 'wms layer - test',
            'type': 'WMS layer',
            'description': 'testing wms creation',
            'url': 'http://ows.mundialis.de/services/service?',
        }
        self.client.post(reverse('add_wms_layer'), wms)
        wms_layer = WMS.objects.all()[0]
        id = wms_layer.id
        wms_layer = self.client.get(
            reverse('get_wms_layer', kwargs={'id': id})
        )
        self.assertEqual(wms_layer.status_code, status.HTTP_200_OK)

    def create_data(self):
        """helper method - creates one record with as staff and logout"""
        self.client.login(username='test_staff_user', password='Test1234')
        wms = {
            'name': 'wms layer - test',
            'type': 'WMS layer',
            'description': 'testing wms creation',
            'url': 'http://ows.mundialis.de/services/service?',
        }
        self.client.post(reverse('add_wms_layer'), wms)
        wms_layer = WMS.objects.all()[0]
        self.client.logout()
        return wms_layer

    def test_update_wms_layer_staff_user(self):
        """updates the layer with staff user"""
        wms_layer = self.create_data()
        self.client.login(username='test_staff_user', password='Test1234')
        id = wms_layer.id
        wms_layer.name = 'updated wms layer name'
        wms_layer = model_to_dict(wms_layer)
        wms_layer['extent'] = ''
        response = self.client.put(
            reverse('edit_wms_layer', kwargs={'id': id}), wms_layer
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'updated wms layer name')

    def test_update_wms_layer_non_staff_user(self):
        """updates the layer with non staff user"""
        wms_layer = self.create_data()
        id = wms_layer.id
        wms_layer.name = 'updated wms layer name'
        wms_layer = model_to_dict(wms_layer)
        wms_layer['extent'] = ''
        self.client.logout()
        self.client.login(username='test_user', password='Test1234')
        response = self.client.put(
            reverse('edit_wms_layer', kwargs={'id': id}), wms_layer
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_wms_layer_anonymous_user(self):
        """updates the layer with anonymous user"""
        wms_layer = self.create_data()
        id = wms_layer.id
        wms_layer.name = 'updated wms layer name'
        wms_layer = model_to_dict(wms_layer)
        wms_layer['extent'] = ''
        self.client.logout()
        response = self.client.put(
            reverse('edit_wms_layer', kwargs={'id': id}), wms_layer
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_wms_layer_staff_user(self):
        """delete the layer with staff user"""
        wms_layer = self.create_data()
        self.client.login(username='test_staff_user', password='Test1234')
        id = wms_layer.id
        response = self.client.get(
            reverse('delete_wms_layer', kwargs={'id': id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_wms_layer_non_staff_user(self):
        """delete the layer with non staff user"""
        wms_layer = self.create_data()
        self.client.login(username='test_user', password='Test1234')
        id = wms_layer.id
        response = self.client.get(
            reverse('delete_wms_layer', kwargs={'id': id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_wms_layer_non_authorized_user(self):
        """delete the layer with non staff user"""
        wms_layer = self.create_data()
        id = wms_layer.id
        response = self.client.get(
            reverse('delete_wms_layer', kwargs={'id': id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
