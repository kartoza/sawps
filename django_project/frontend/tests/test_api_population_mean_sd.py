import base64

from django.urls import reverse

from django.contrib.auth.models import User
from django.test import Client
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient

from population_data.factories import AnnualPopulationF
from property.factories import PropertyFactory
from property.models import Province
from regulatory_permit.models import DataUsePermission
from species.factories import TaxonRankFactory
from species.models import TaxonRank, Taxon
from stakeholder.models import Organisation


class PopulationMeanSDChartApiTest(APITestCase):
    def setUp(self):
        self.url = reverse('population-mean-sd-chart')
        self.user = User.objects.create_user(
            username='testuserd',
            password='testpasswordd',
            is_superuser=True
        )
        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +
                                  base64.b64encode(b'testuserd:testpasswordd').decode('ascii'),
        }
        self.client = Client()
        session = self.client.session
        session.save()


        taxon_rank = TaxonRank.objects.filter(name="Species").first()
        if not taxon_rank:
            taxon_rank = TaxonRankFactory.create(name="Species")

        self.taxon = Taxon.objects.create(
            taxon_rank=taxon_rank, common_name_verbatim="Lion",
            scientific_name="Penthera leo"
        )
        self.organisation = Organisation.objects.create(
            name="test_organisation"
        )
        self.province1 = Province.objects.create(name="Province1")
        self.property1 = PropertyFactory.create(name="Property 1", province=self.province1, organisation=self.organisation)

        AnnualPopulationF.create(
            year=2021,
            property=self.property1,
            user=self.user,
            taxon=self.taxon,
            total=60,
            adult_male=50,
            adult_female=10,
            juvenile_male=15,
            juvenile_female=20,
            juvenile_total=35,
            sub_adult_total=20,
            sub_adult_male=10,
            sub_adult_female=10,
        )
        AnnualPopulationF.create(
            year=2022,
            property=self.property1,
            user=self.user,
            taxon=self.taxon,
            total=20,
            adult_male=10,
            adult_female=10,
            juvenile_male=15,
            juvenile_female=25,
            juvenile_total=40,
            sub_adult_total=40,
            sub_adult_male=30,
            sub_adult_female=10,
        )
        AnnualPopulationF.create(
            year=1960,
            property=self.property1,
            user=self.user,
            taxon=self.taxon,
            total=50,
            adult_male=30,
            adult_female=20,
            juvenile_male=50,
            juvenile_female=60,
            juvenile_total=110,
            sub_adult_male=None,
            sub_adult_female=None,
            sub_adult_total=None
        )

    def test_get_population_data(self):
        data = {
            'species': "Penthera leo"
        }
        response = self.client.get(self.url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(
            response.data[self.property1.property_type.name]['mean_adult_male'],
            300.0
        )
        self.assertGreater(
            response.data[self.property1.property_type.name]['sd_adult_female'],
            50
        )

