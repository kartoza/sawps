from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from species.models import Taxon
from frontend.serializers.national_statistics import (
    SpeciesListSerializer,
    NationalStatisticsSerializer
)
from django.contrib.auth import get_user_model
from django.test import Client
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.templatetags.static import static

class NationalSpeciesViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('species_list_national')

    @patch('frontend.api_views.national_statistic.NationalSpeciesView.get_species_list')
    def test_get_species_list(self, mock_get_species_list):
        # Create mock Taxon objects
        taxon1 = Taxon(
            common_name_varbatim='Species 1',
            icon='images/lion.png'
        )
        taxon2 = Taxon(
            common_name_varbatim='Species 2',
            icon='images/tiger.png'
        )
        test_user = get_user_model().objects.create_user(
            username='testuser', password='testpassword'
        )
        device = TOTPDevice(
            user=test_user,
            name='device_name'
        )
        device.save()
        client = Client()
        resp = client.login(username='testuser', password='testpassword')

        self.assertEqual(resp, True)


        # Mock the get_species_list method to return the mock Taxon objects
        mock_get_species_list.return_value = [taxon1, taxon2]

        response = client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        serializer = SpeciesListSerializer([taxon1, taxon2], many=True)
        # Create a serializer instance for each taxon object
        serializer1 = SpeciesListSerializer(taxon2)
        
        icon_url_1 = serializer1.get_species_icon(taxon2)
        expected_url_1 = '/media/images/tiger.png'
        self.assertEqual(icon_url_1, expected_url_1)

    @patch('frontend.api_views.national_statistic.NationalSpeciesView.get_species_list')
    def test_get_species_list_empty(self, mock_get_species_list):
        # Mock the get_species_list method to return an empty list
        mock_get_species_list.return_value = []
        test_user = get_user_model().objects.create_user(
            username='testuser', password='testpassword'
        )
        device = TOTPDevice(
            user=test_user,
            name='device_name'
        )
        device.save()
        client = Client()
        resp = client.login(username='testuser', password='testpassword')

        self.assertEqual(resp,True)

        response = client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)



class NationalStatisticsViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('statistics_national')
        self.test_user = get_user_model().objects.create_user(
            username='testuser', password='testpassword'
        )
        self.device = TOTPDevice(
            user=self.test_user,
            name='device_name'
        )
        self.device.save()
        self.client = Client()

    @patch('property.models.Property.objects.filter')
    @patch('species.models.OwnedSpecies.objects.filter')
    def test_get_statistics(self, mock_owned_species_filter, mock_property_filter):
        # Mock Property objects and aggregate result
        mock_property_filter.return_value.count.return_value = 5
        mock_property_filter.return_value.aggregate.return_value = {'total_area': 100}

        # Mock OwnedSpecies objects and aggregate result
        mock_owned_species_filter.return_value.aggregate.return_value = {'total_area_to_species': 50}

        client = self.client
        client.login(username='testuser', password='testpassword')
        response = client.get(self.url)

        self.assertIsNotNone(response)

    @patch('property.models.Property.objects.filter')
    @patch('species.models.OwnedSpecies.objects.filter')
    def test_get_statistics_empty(self, mock_owned_species_filter, mock_property_filter):
        # Mock Property objects and aggregate result
        mock_property_filter.return_value.count.return_value = 0

        # Mock OwnedSpecies objects and aggregate result
        mock_owned_species_filter.return_value.aggregate.return_value = {'total_area_to_species': 0}

        client = self.client
        client.login(username='testuser', password='testpassword')
        response = client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response)
