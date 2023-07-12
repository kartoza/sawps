import base64
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from species.factories import OwnedSpeciesFactory

class OwnedSpeciesTestCase(TestCase):
    def setUp(self):
        self.owned_species = OwnedSpeciesFactory.create_batch(5)
        self.url = reverse('data-table')
        
        user = User.objects.create_user(
                username='testuserd',
                password='testpasswordd'
            )
        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +
            base64.b64encode(b'testuserd:testpasswordd').decode('ascii'),
        }
        self.client = Client()

    def test_list_owned_species(self):
        url = self.url
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_filter_by_species_name(self):
        owned_species = OwnedSpeciesFactory(taxon__common_name_varbatim='SpeciesA')
        url = self.url
        data = {'species': 'SpeciesA'}
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['taxon']['common_name_varbatim'],
            owned_species.taxon.common_name_varbatim
        )

    def test_filter_by_month(self):
        owned_species = OwnedSpeciesFactory()
        url = self.url
        data = {
            'month': owned_species.annualpopulation_set.first().month.name,
            'start_year':owned_species.annualpopulation_set.first().year,
            'end_year':owned_species.annualpopulation_set.first().year
            }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['annualpopulation']['month'],
            owned_species.annualpopulation_set.first().month.name
        )

    def test_filter_by_name_month_and_property(self):
        owned_species = OwnedSpeciesFactory(
            taxon__common_name_varbatim='SpeciesA',
            property__name='PropertyA'
        )
        url = self.url
        data = {
            'species': 'SpeciesA',
            'property': 'PropertyA',
            'month': owned_species.annualpopulation_set.first().month.name,
            'start_year':owned_species.annualpopulation_set.first().year,
            'end_year':owned_species.annualpopulation_set.first().year,
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['property']['name'],
            owned_species.property.name
        )
        self.assertEqual(
            response.data[0]['annualpopulation']['month'],
            owned_species.annualpopulation_set.first().month.name
        )

    def test_filter_by_annualpopulation_category(self):
        owned_species = OwnedSpeciesFactory(
            taxon__common_name_varbatim='SpeciesA',
            property__name='PropertyA'
        )
        url = self.url
        data = {
            'total':owned_species.annualpopulation_set.first().total,
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]['annualpopulation']['total'],
            owned_species.annualpopulation_set.first().total
        )
