import base64

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from frontend.utils.organisation import CURRENT_ORGANISATION_ID_KEY
from property.factories import PropertyFactory
from rest_framework import status
from species.factories import OwnedSpeciesFactory, TaxonFactory, TaxonRankFactory
from species.models import TaxonRank
from stakeholder.factories import organisationFactory, organisationUserFactory


class BaseTestCase(TestCase):
    def setUp(self):
        """
        Set up test data and environment for the test cases.

        This method creates necessary test objects like TaxonRank, Taxon, User, Organisation,
        Property, and OwnedSpecies. It also sets up the client and session for testing.
        """
        taxon_rank = TaxonRank.objects.filter(name="Species").first()
        if not taxon_rank:
            taxon_rank = TaxonRankFactory.create(name="Species")

        self.taxon = TaxonFactory.create(
            taxon_rank=taxon_rank, common_name_varbatim="Lion"
        )

        self.user = User.objects.create_user(
            username="testuserd",
            password="testpasswordd"
        )

        self.organisation_1 = organisationFactory.create()
        organisationUserFactory.create(
            user=self.user,
            organisation=self.organisation_1
        )

        self.property = PropertyFactory.create(
            organisation=self.organisation_1, name="PropertyA"
        )

        self.owned_species = OwnedSpeciesFactory.create_batch(
            5, taxon=self.taxon, user=self.user, property=self.property
        )

        self.auth_headers = {
            "HTTP_AUTHORIZATION": "Basic "
            + base64.b64encode(b"testuserd:testpasswordd").decode("ascii"),
        }
        self.client = Client()

        session = self.client.session
        session[CURRENT_ORGANISATION_ID_KEY] = self.organisation_1.id
        session.save()


class SpeciesPopuationCountPerYearTestCase(BaseTestCase):
    """
    Test the species population count API endpoint.
    """
    def setUp(self) -> None:
        """
        Set up the test case.
        """
        super().setUp()
        self.url = reverse("species_population_count")

    def test_species_population_count(self) -> None:
        """
        Test species population count.
        """
        url = self.url
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get('species_name'), 'Lion')
        self.assertEqual(
            response.data[0]['annualpopulation_count'][0].get('year_total'),
            100
        )

    def test_species_population_count_filter_by_name(self) -> None:
        """
        Test species population count filtered by species name.
        """
        data = {'species': 'Lion'}
        url = self.url
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['species_name'], 'Lion')

    def test_species_population_count_filter_by_property(self) -> None:
        """
        Test species population count filtered by property.
        """
        id = self.owned_species[0].property_id
        data = {'property':id}
        url = self.url
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]['annualpopulation_count'][0].get('year_total'),
            100
        )

    def test_species_population_count_filter_by_year(self) -> None:
        """
        Test species population count filtered by year.
        """
        year = self.owned_species[1].annualpopulation_set.first().year
        data = {'start_year': year, "end_year":year}
        url = self.url
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]['annualpopulation_count'][0].get('year'),
            year
        )


class ActivityPercentageTestCase(BaseTestCase):
    """
    Test the activity percentage API endpoint.
    """
    def setUp(self) -> None:
        """
        Set up the test case.
        """
        super().setUp()
        self.url = reverse("activity_percentage")

    def test_activity_percentage(self) -> None:
        """
        Test activity percentage calculation.
        """
        url = self.url
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'][0]['total'], 500)
        self.assertEqual(
            list(response.data['data'][0]['activities'][0].values())[0], 20.0
        )

    def test_activity_percentage_filter_by_year(self) -> None:
        """
        Test activity percentage calculation with year-based filters.
        """
        year = self.owned_species[1].annualpopulationperactivity_set.first().year
        data = {'start_year': year, "end_year":year}
        url = self.url
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get('data')[0].get('total'), 500)


class TotalCountPerActivityTestCase(BaseTestCase):
    """
    Test the total count per activity API endpoint.
    """
    def setUp(self) -> None:
        """
        Set up the test case.
        """
        super().setUp()
        self.url = reverse("total_count_per_activity")

    def test_total_count_per_activity(self) -> None:
        """
        Test total count per activity calculation.
        """
        url = self.url
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[0]['activities']), 5)
        self.assertEqual(list(response.data[0]['activities'][0].values())[0], 100)


class SpeciesPopulationTotalAndDensityTestCase(BaseTestCase):
    """
    Test the species population total density API endpoint.
    """
    def setUp(self) -> None:
        """
        Set up the test case.
        """
        super().setUp()
        self.url = reverse("species_population_total_density")

    def test_species_population_total_and_density(self) -> None:
        """
        Test species population total and density calculation.
        """
        url = self.url
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]['density'].get('density'), 0.5
        )
        self.assertEqual(
            response.data[0]['density'].get('total'), 100
        )


class PropertiesPerPopulationCategoryTestCase(BaseTestCase):
    """
    Test case for the endpoint that retrieves
    properties population categories.
    """
    def setUp(self) -> None:
        """
        Set up the test case.
        """
        super().setUp()
        self.url = reverse("properties_per_population_category")

    def test_species_population_total_and_density(self) -> None:
        """
        Test species population categories.
        """
        url = self.url
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['>200'], 1)

    def test_properties_population_category_filter_by_property(self) -> None:
        """
        Test species population categories filtered by property.
        """
        id = self.owned_species[0].property_id
        data = {'property':id}
        url = self.url
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['1-10'], 0)
