import mock
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import status

from frontend.api_views.spatial_filter import SpatialLayerSerializer
from frontend.tests.model_factories import LayerF, UserF


def mocked_process_func(*args, **kwargs):
    return True


class SpatialLayerSerializerTestCase(TestCase):

    def setUp(self):
        self.layer1 = LayerF.create(
            layer_title='Layer 1',
            name='test'
        )

    def test_serializer(self):
        serialized_layer = SpatialLayerSerializer(self.layer1).data
        self.assertEqual(serialized_layer['layer_title'], "Layer 1")


class SpatialFilterListViewTestCase(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(
            self.username, password=self.password)
        device = TOTPDevice(
            user=self.user,
            name='device_name'
        )
        device.save()
        self.client.login(username=self.username, password=self.password)

        self.layer1 = LayerF.create(layer_title="Layer 1", is_filter_layer=True)
        self.layer2 = LayerF.create(layer_title="Layer 2", is_filter_layer=False)

    def test_get_spatial_filter_list(self):
        url = reverse('spatial-filter-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['layer_title'], "Layer 1")


class SpatialFilterLayerTestCase(TestCase):

    def setUp(self) -> None:
        self.superuser = UserF.create(
            username='test_2',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        TOTPDevice.objects.create(
            user=self.superuser, name='Test Device', confirmed=True)

    @mock.patch('frontend.admin.generate_spatial_filter_for_all_properties.delay')
    def test_has_no_valid_layer(self, mocked_process):
        mocked_process.side_effect = mocked_process_func
        layer = LayerF.create(
            layer_title='Layer 1',
            name='test',
            spatial_filter_field=''
        )
        client = Client()
        client.force_login(self.superuser)
        response = client.post(
            reverse('admin:frontend_layer_changelist'),
            {
                'action': 'trigger_generate_spatial_filter',
                '_selected_action': [layer.id]
            },
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mocked_process.assert_not_called()

    @mock.patch('frontend.admin.generate_spatial_filter_for_all_properties.delay')
    def test_valid_layer(self, mocked_process):
        mocked_process.side_effect = mocked_process_func
        layer = LayerF.create(
            layer_title='Layer 1',
            name='test',
            spatial_filter_field='test'
        )
        client = Client()
        client.force_login(self.superuser)
        response = client.post(
            reverse('admin:frontend_layer_changelist'),
            {
                'action': 'trigger_generate_spatial_filter',
                '_selected_action': [layer.id]
            },
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mocked_process.assert_called_once()
