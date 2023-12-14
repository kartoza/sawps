from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.test import Client
from django.shortcuts import reverse
from population_data.factories import AnnualPopulationF
from property.factories import PropertyFactory
from property.models import Property, Province
from species.factories import (
    TaxonRankFactory
)
import base64
from species.models import Taxon, TaxonRank
from stakeholder.models import Organisation
import base64

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from frontend.static_mapping import (
    NATIONAL_DATA_SCIENTIST
)
from population_data.factories import (
    AnnualPopulationF
)
from activity.models import ActivityType
from population_data.models import AnnualPopulationPerActivity
from property.factories import PropertyFactory

from sawps.tests.models.account_factory import GroupF
from species.factories import (
    TaxonRankFactory
)
from species.models import TaxonRank
from stakeholder.factories import (
    organisationUserFactory,
)
from frontend.tests.model_factories import (
    SpatialDataModelF,
    SpatialDataModelValueF
)


class SpeciesCountPerProvinceTest(APITestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(
            name="test_organisation"
        )

        taxon_rank = TaxonRank.objects.filter(name="Species").first()
        if not taxon_rank:
            taxon_rank = TaxonRankFactory.create(name="Species")

        self.taxon = Taxon.objects.create(
            taxon_rank=taxon_rank, common_name_verbatim="Lion",
            scientific_name="Penthera leo"
        )

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

        # add user 1 to organisation 1 and 3
        organisationUserFactory.create(
            user=self.user,
            organisation=self.organisation
        )
        group = GroupF.create(name=NATIONAL_DATA_SCIENTIST)
        self.user.groups.add(group)
        self.user.user_profile.current_organisation = self.organisation
        self.user.save()

        self.province1 = Province.objects.create(name="Province1")
        self.province2 = Province.objects.create(name="Province2")

        # Create test data, including properties and owned species
        self.property1 = PropertyFactory.create(
            name="Property 1",
            province=self.province1,
            organisation=self.organisation
        )
        self.property2 = PropertyFactory.create(
            name="Property 2",
            province=self.province2,
            organisation=self.organisation
        )
        self.property3 = PropertyFactory.create(
            name="Property 3",
            province=self.province2,
            organisation=self.organisation
        )

        self.pop1 = AnnualPopulationF.create(
            year=2023,
            property=self.property3,
            user=self.user,
            taxon=self.taxon,
            total=60,
            adult_male=10,
            adult_female=10,
            juvenile_male=10,
            juvenile_female=10,
            sub_adult_total=10,
            sub_adult_male=10,
            sub_adult_female=10,
            juvenile_total=10,
        )
        self.pop2 = AnnualPopulationF.create(
            year=2023,
            property=self.property1,
            user=self.user,
            taxon=self.taxon,
            total=60,
            adult_male=10,
            adult_female=10,
            juvenile_male=10,
            juvenile_female=10,
            sub_adult_total=10,
            sub_adult_male=10,
            sub_adult_female=10,
            juvenile_total=10,
        )
        self.pop3 = AnnualPopulationF.create(
            year=2023,
            property=self.property2,
            user=self.user,
            taxon=self.taxon,
            total=10,
            adult_male=5,
            adult_female=5
        )

        self.pop4 = AnnualPopulationF.create(
            year=2022,
            property=self.property1,
            user=self.user,
            taxon=self.taxon,
            total=20,
            adult_male=10,
            adult_female=10,
            juvenile_male=10,
            juvenile_female=10,
            sub_adult_total=10,
            sub_adult_male=10,
            sub_adult_female=10,
            juvenile_total=10,
        )

        self.pop5 = AnnualPopulationF.create(
            year=1960,
            property=self.property1,
            user=self.user,
            taxon=self.taxon,
            total=30,
            adult_male=10,
            adult_female=10,
            juvenile_male=10,
            juvenile_female=10,
            sub_adult_total=10,
            sub_adult_male=10,
            sub_adult_female=10,
            juvenile_total=10,
        )
        # clear post generation activities
        self.pop1.annualpopulationperactivity_set.all().delete()
        self.pop2.annualpopulationperactivity_set.all().delete()
        self.pop3.annualpopulationperactivity_set.all().delete()
        self.pop4.annualpopulationperactivity_set.all().delete()
        self.pop5.annualpopulationperactivity_set.all().delete()
        # add activity
        self.activity_type1 = ActivityType.objects.create(name='test_activity1')
        self.activity_type2 = ActivityType.objects.create(name='test_activity2')
        AnnualPopulationPerActivity.objects.create(
            activity_type=self.activity_type1,
            annual_population=self.pop1,
            intake_permit='1',
            offtake_permit='1',
            total=15,
            year=self.pop1.year
        )
        AnnualPopulationPerActivity.objects.create(
            activity_type=self.activity_type2,
            annual_population=self.pop1,
            intake_permit='1',
            offtake_permit='1',
            total=25,
            year=self.pop1.year
        )
        # add spatial value for property3
        spatial_data = SpatialDataModelF.create(
            property=self.property3
        )
        self.spatial_value1 = 'spatial filter test 1'
        self.spatial_value2 = 'spatial filter test 2'
        SpatialDataModelValueF.create(
            spatial_data=spatial_data,
            context_layer_value=self.spatial_value1
        )
        SpatialDataModelValueF.create(
            spatial_data=spatial_data,
            context_layer_value=self.spatial_value1
        )

        self.url = reverse('species_count_per_province')
        self.organisations = [self.organisation.id]

    def test_calculate_species_count_per_province(self):
        data = {
            "species": "Penthera leo",
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)])
        }
        # self.client.force_login(self.user)
        response = self.client.get(self.url, data, **self.auth_headers)
        result_data = response.json()

        # Perform assertions based on the expected results
        # We have two provinces with 3 years of data
        # For 2023, there are data for Province1 and Province2
        # In 2023, Province 1 population is 60 coming from Property 1
        # In 2023 Province 2 population is 70, coming from Property 1 (60) and Property 2 (10)
        self.assertEqual(
            result_data,
            [
                {"year": 2023, "count": 70, "province": "Province2", "species": "Penthera leo"},
                {"year": 2023, "count": 60, "province": "Province1", "species": "Penthera leo"},
                {"year": 2022, "count": 20, "province": "Province1", "species": "Penthera leo"},
                {"year": 1960, "count": 30, "province": "Province1", "species": "Penthera leo"},
            ]
        )

    def test_calculate_species_count_per_province_year_filter(self):
        data = {
            "species": "Penthera leo",
            "start_year": 2023,
            "end_year": 2023,
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)])
        }
        # self.client.force_login(self.user)
        response = self.client.get(self.url, data, **self.auth_headers)
        result_data = response.json()

        # Perform assertions based on the expected results
        self.assertEqual(len(result_data), 2)  # We have two provinces with population data

        self.assertEqual(
            result_data,
            [
                {"year": 2023, "count": 70, "province": "Province2", "species": "Penthera leo"},
                {"year": 2023, "count": 60, "province": "Province1", "species": "Penthera leo"},
            ]
        )

    def test_calculate_species_count_per_province_activity_filter(self):
        data = {
            "species": "Penthera leo",
            "start_year": 2023,
            "end_year": 2023,
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)]),
            "activity": f'{self.activity_type1.id},{self.activity_type2.id}'
        }
        # self.client.force_login(self.user)
        response = self.client.get(self.url, data, **self.auth_headers)
        result_data = response.json()

        # Perform assertions based on the expected results
        self.assertEqual(len(result_data), 1)

        self.assertEqual(
            result_data,
            [
                {"year": 2023, "count": 60, "province": "Province2", "species": "Penthera leo"},
            ]
        )

    def test_calculate_species_count_per_province_spatial_filter(self):
        data = {
            "species": "Penthera leo",
            "start_year": 2023,
            "end_year": 2023,
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)]),
            "spatial_filter_values": f"{self.spatial_value1},{self.spatial_value2}"
        }
        # self.client.force_login(self.user)
        response = self.client.get(self.url, data, **self.auth_headers)
        result_data = response.json()

        # Perform assertions based on the expected results
        self.assertEqual(len(result_data), 1)

        self.assertEqual(
            result_data,
            [
                {"year": 2023, "count": 60, "province": "Province2", "species": "Penthera leo"},
            ]
        )
