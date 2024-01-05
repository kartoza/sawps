import unittest
from django.http import HttpRequest
from population_data.models import PopulationEstimateCategory
from frontend.serializers.metrics import TotalCountPerPopulationEstimateSerializer
from django.test import TestCase, Client
from stakeholder.models import Organisation
from property.factories import PropertyFactory
from species.factories import (
    TaxonRankFactory
)
from activity.models import ActivityType
from species.models import Taxon, TaxonRank
from population_data.models import AnnualPopulationPerActivity
from population_data.factories import AnnualPopulationF
import base64
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from frontend.tests.model_factories import (
    SpatialDataModelF,
    SpatialDataModelValueF
)


class TotalCountPerPopulationEstimateSerializerTestCase(TestCase):
    def setUp(self):
        # Create and set up test data, such as AnnualPopulation records
        self.species_name = "TestSpecies"
        self.property_ids = [1, 2]
        self.start_year = 2020
        self.end_year = 2022

        # Create an instance of the serializer
        self.serializer = TotalCountPerPopulationEstimateSerializer(
            context={
                "request": HttpRequest(),
            }
        )
        organisation = Organisation.objects.create(
            name="test_organisation"
        )

        taxon_rank = TaxonRank.objects.filter(name="Species").first()
        if not taxon_rank:
            taxon_rank = TaxonRankFactory.create(name="Species")

        taxon = Taxon.objects.create(
            taxon_rank=taxon_rank, common_name_verbatim="Lion",
            scientific_name="Penthera leo"
        )

        self.user = User.objects.create_user(
            username="testuserd",
            password="testpasswordd"
        )

        # Create test data, including properties and owned species
        self.property1 = PropertyFactory.create(name="Property 1", organisation=organisation)
        self.property2 = PropertyFactory.create(name="Property 2", organisation=organisation)
        self.property3 = PropertyFactory.create(name="Property 3", organisation=organisation)

        self.category_a = PopulationEstimateCategory.objects.create(name="Category A")
        self.category_b = PopulationEstimateCategory.objects.create(name="Category B")

        self.pop1 = AnnualPopulationF.create(
            year=2020,
            property=self.property1,
            user=self.user,
            taxon=taxon,
            total=100,
            adult_male=10,
            adult_female=10,
            juvenile_male=10,
            juvenile_female=10,
            sub_adult_total=10,
            sub_adult_male=10,
            sub_adult_female=10,
            juvenile_total=10,
            population_estimate_category=self.category_a
        )

        self.pop2 = AnnualPopulationF.create(
            year=2022,
            property=self.property1,
            user=self.user,
            taxon=taxon,
            total=100,
            adult_male=10,
            adult_female=10,
            juvenile_male=10,
            juvenile_female=10,
            sub_adult_total=10,
            sub_adult_male=10,
            sub_adult_female=10,
            juvenile_total=10,
            population_estimate_category=self.category_a
        )

        self.pop3 = AnnualPopulationF.create(
            year=2020,
            property=self.property2,
            user=self.user,
            taxon=taxon,
            total=100,
            adult_male=10,
            adult_female=10,
            juvenile_male=10,
            juvenile_female=10,
            sub_adult_total=10,
            sub_adult_male=10,
            sub_adult_female=10,
            juvenile_total=10,
            population_estimate_category=self.category_a
        )

        self.pop4 = AnnualPopulationF.create(
            year=2022,
            property=self.property3,
            user=self.user,
            taxon=taxon,
            total=200,
            adult_male=10,
            adult_female=10,
            juvenile_male=10,
            juvenile_female=10,
            sub_adult_total=10,
            sub_adult_male=10,
            sub_adult_female=10,
            juvenile_total=10,
            population_estimate_category=self.category_a
        )

        self.pop5 = AnnualPopulationF.create(
            year=2022,
            property=self.property2,
            user=self.user,
            taxon=taxon,
            total=100,
            adult_male=10,
            adult_female=10,
            juvenile_male=10,
            juvenile_female=10,
            sub_adult_total=10,
            sub_adult_male=10,
            sub_adult_female=10,
            juvenile_total=10,
            population_estimate_category=self.category_b
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
            annual_population=self.pop2,
            intake_permit='1',
            offtake_permit='1',
            total=15,
            year=self.pop2.year
        )
        AnnualPopulationPerActivity.objects.create(
            activity_type=self.activity_type2,
            annual_population=self.pop2,
            intake_permit='1',
            offtake_permit='1',
            total=25,
            year=self.pop2.year
        )
        # add spatial value for property1
        spatial_data = SpatialDataModelF.create(
            property=self.property1
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

    def test_get_total_counts_per_population_estimate(self):
        data = {
            'species': "Penthera leo",
            'property': f"{self.property1.id},{self.property2.id},{self.property3.id}",
            'start_year': "2020",
            'end_year': "2022"
        }
        auth_headers = {
            "HTTP_AUTHORIZATION": "Basic "
                                  + base64.b64encode(b"testuserd:testpasswordd").decode("ascii"),
        }
        client = Client()

        session = client.session
        session.save()

        url = reverse("total-count-per-population-estimate")
        response = client.get(url, data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Call the method you want to test
        result = response.data

        # Define the expected result
        expected_result = {
            'Category A': {
                'count': 2,
                'percentage': 0.66,
                'total': 300,
                'years': [2022],
            },
            'Category B': {
                'count': 1,
                'percentage': 1.0,
                'total': 100,
                'years': [2022],
            },
        }

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

    def test_empty_data(self):
        # Test when there's no data
        result = self.serializer.get_total_counts_per_population_estimate()
        self.assertEqual(result, {}) 

    def test_invalid_species_name(self):
        # Test with an invalid species name
        self.serializer.context["request"].GET["species"] = "NonExistentSpecies"
        result = self.serializer.get_total_counts_per_population_estimate()
        self.assertEqual(result, {})

    def test_invalid_property_ids(self):
        # Test with invalid property IDs
        self.serializer.context["request"].GET["property"] = "100,200,300"
        result = self.serializer.get_total_counts_per_population_estimate()
        self.assertEqual(result, {})

    def test_get_total_counts_per_pop_estimate_with_act_filter(self):
        data = {
            'species': "Penthera leo",
            'property': f"{self.property1.id},{self.property2.id},{self.property3.id}",
            'start_year': "2020",
            'end_year': "2022",
            'activity': f"{self.activity_type1.id},{self.activity_type2.id}"
        }

        auth_headers = {
            "HTTP_AUTHORIZATION": "Basic "
                                  + base64.b64encode(b"testuserd:testpasswordd").decode("ascii"),
        }
        client = Client()

        session = client.session
        session.save()

        url = reverse("total-count-per-population-estimate")
        response = client.get(url, data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Call the method you want to test
        result = response.data
        # Define the expected result
        expected_result = {
            'Category A': {
                'count': 1,
                'percentage': 1.0,
                'total': 100,
                'years': [2022],
            }
        }

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

    def test_get_total_counts_per_pop_estimate_with_spatial_filter(self):
        data = {
            'species': "Penthera leo",
            'property': f"{self.property1.id},{self.property2.id},{self.property3.id}",
            'start_year': "2020",
            'end_year': "2022",
            'spatial_filter_values': f"{self.spatial_value1},{self.spatial_value2}"
        }

        auth_headers = {
            "HTTP_AUTHORIZATION": "Basic "
                                  + base64.b64encode(b"testuserd:testpasswordd").decode("ascii"),
        }
        client = Client()

        session = client.session
        session.save()

        url = reverse("total-count-per-population-estimate")
        response = client.get(url, data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Call the method you want to test
        result = response.data
        # Define the expected result
        expected_result = {
            'Category A': {
                'count': 1,
                'percentage': 1.0,
                'total': 100,
                'years': [2022],
            }
        }

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
