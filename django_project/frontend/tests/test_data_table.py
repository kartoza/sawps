import base64

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django_otp.plugins.otp_totp.models import TOTPDevice
from property.factories import PropertyFactory
from rest_framework import status
from species.factories import OwnedSpeciesFactory, TaxonFactory, TaxonRankFactory
from species.models import TaxonRank
from stakeholder.factories import (
    organisationFactory,
    organisationUserFactory,
    userRoleTypeFactory,
)
from stakeholder.models import UserProfile


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
        self.role_organisation_manager = userRoleTypeFactory.create(
            name='Organisation manager',
        )
        UserProfile.objects.create(
            user=user,
            current_organisation=self.organisation_1,
            user_role_type_id=self.role_organisation_manager
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
        session.save()

    def test_data_table_filter_by_species_name(self) -> None:
        """Test data table filter by species name"""
        url = self.url
        data = {'species': 'SpeciesA'}
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["Property_report"][0]["common_name"],
            "SpeciesA"
        )

    def test_filter_by_property(self) -> None:
        """Test data table filter by property"""
        data = {
            'species': self.taxon.common_name_varbatim,
            'property': self.property.id,
            'start_year': self.owned_species[0].annualpopulation_set.first().year,
            'end_year': self.owned_species[0].annualpopulation_set.first().year,
        }
        response = self.client.get(self.url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["Property_report"][0]["property_name"],
            "PropertyA"
        )

    def test_filter_by_year_and_report(self) -> None:
        """Test data table filter by year and report"""
        year = self.owned_species[1].annualpopulation_set.first().year
        data = {
            "start_year": year,
            "end_year":year,
            "reports": "Species_population_report"
        }
        url = self.url
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["Species_population_report"][0]["year"],
            year
        )

    def test_national_user_role(self) -> None:
        """Test data table filter by national user"""
        user_national = User.objects.create_user(
            username='national_user',
            password='national_pass'
        )
        self.role_national_user = userRoleTypeFactory.create(
            name='National user',
        )
        self.user_profile_national = UserProfile.objects.create(
            user=user_national,
            user_role_type_id=self.role_national_user
        )
        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +
            base64.b64encode(b'national_user:national_pass').decode('ascii'),
        }
        url = self.url
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "")

    def test_regional_user_role(self) -> None:
        """Test data table filter by regional user"""
        user_regional = User.objects.create_user(
            username='regional_user',
            password='regional_pass'
        )
        self.role_regional_user = userRoleTypeFactory.create(
            name='Regional user',
        )
        self.user_profile_regional = UserProfile.objects.create(
            user=user_regional,
            user_role_type_id=self.role_regional_user
        )

        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +
            base64.b64encode(b'regional_user:regional_pass').decode('ascii'),
        }
        url = self.url
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "")

    def test_data_table_activity_report(self) -> None:
        """Test data table activity report"""
        url = self.url
        data = {
            "species": "SpeciesA",
            "reports": "Activity_report",
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["Activity_report"].get(
                "Planned_euthanasia"
            )[0].get("property_name"),
            "PropertyA"
        )

    def test_data_table_sampling_report(self) -> None:
        """Test data table sampling report"""
        url = self.url
        data = {
            "species": "SpeciesA",
            "reports": "Sampling_report",
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["Sampling_report"][0]["common_name"],
            "SpeciesA"
        )
