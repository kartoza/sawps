import base64
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from species.models import TaxonRank
from frontend.utils.organisation import CURRENT_ORGANISATION_ID_KEY
from species.factories import (
    OwnedSpeciesFactory, TaxonFactory, TaxonRankFactory,
)
from stakeholder.factories import (
    organisationFactory,
    organisationUserFactory
)
from property.factories import PropertyFactory


class OwnedSpeciesTestCase(TestCase):
    def setUp(self):
        taxon_rank = TaxonRank.objects.filter(
            name='Species'
        ).first()
        if not taxon_rank:
            taxon_rank = TaxonRankFactory.create(
                name='Species'
            )
        self.taxon = TaxonFactory.create(
            taxon_rank=taxon_rank,
            common_name_varbatim='SpeciesA'
        )
        user = User.objects.create_user(
                username='testuserd',
                password='testpasswordd'
            )
        self.organisation_1 = organisationFactory.create()
        # add user 1 to organisation 1 and 3
        organisationUserFactory.create(
            user=user,
            organisation=self.organisation_1
        )
        self.property = PropertyFactory.create(
            organisation=self.organisation_1,
            name='PropertyA'
        )
        self.owned_species = OwnedSpeciesFactory.create_batch(
            5, taxon=self.taxon, user=user, property=self.property)
        self.url = reverse('data-table')
        
        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +
            base64.b64encode(b'testuserd:testpasswordd').decode('ascii'),
        }
        self.client = Client()

        session = self.client.session
        session[CURRENT_ORGANISATION_ID_KEY] = self.organisation_1.id
        session.save()


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
        self.assertGreater(len(response.data), 0)
        self.assertEqual(
            response.data[0]['taxon']['common_name_varbatim'],
            owned_species.taxon.common_name_varbatim
        )

    def test_filter_by_month(self):
        url = self.url
        data = {
            'month': self.owned_species[0].annualpopulation_set.first().month.name,
            'start_year': self.owned_species[0].annualpopulation_set.first().year,
            'end_year': self.owned_species[0].annualpopulation_set.first().year
            }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['annualpopulation']['month'],
            self.owned_species[0].annualpopulation_set.first().month.name
        )

    def test_filter_by_name_month_and_property(self):
        data = {
            'species': self.taxon.common_name_varbatim,
            'property': self.property.name,
            'month': self.owned_species[0].annualpopulation_set.first().month.name,
            'start_year': self.owned_species[0].annualpopulation_set.first().year,
            'end_year': self.owned_species[0].annualpopulation_set.first().year,
        }
        response = self.client.get(self.url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertEqual(
            response.data[0]['property']['name'],
            self.owned_species[0].property.name
        )
        self.assertEqual(
            response.data[0]['annualpopulation']['month'],
            self.owned_species[0].annualpopulation_set.first().month.name
        )

    def test_filter_by_annualpopulation_category(self):
        data = {
            'total': self.owned_species[0].annualpopulation_set.first().total,
        }
        response = self.client.get(self.url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]['annualpopulation']['total'],
            self.owned_species[0].annualpopulation_set.first().total
        )
