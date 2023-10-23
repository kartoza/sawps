import base64

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from frontend.static_mapping import (
    NATIONAL_DATA_SCIENTIST,
    REGIONAL_DATA_SCIENTIST,
    REGIONAL_DATA_CONSUMER
)
from population_data.models import AnnualPopulationPerActivity
from property.factories import PropertyFactory
from rest_framework import status

from activity.models import ActivityType
from sawps.tests.models.account_factory import GroupF
from species.factories import (
    OwnedSpeciesFactory,
    TaxonFactory,
    TaxonRankFactory
)
from species.models import TaxonRank
from stakeholder.factories import (
    organisationFactory,
    organisationUserFactory,
    userRoleTypeFactory,
)
from property.factories import ProvinceFactory
from frontend.tests.model_factories import (
    SpatialDataModelF,
    SpatialDataModelValueF
)
from stakeholder.models import OrganisationInvites, MANAGER


class OwnedSpeciesTestMixins:

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
            scientific_name='SpeciesA'
        )
        user = User.objects.create_user(
            username='testuserd',
            password='testpasswordd'
        )
        self.province = ProvinceFactory.create(name='Western Cape')
        self.organisation_1 = organisationFactory.create(
            name='OrganisationA',
            province=self.province
        )
        # add user 1 to organisation 1 and 3
        organisationUserFactory.create(
            user=user,
            organisation=self.organisation_1
        )
        group = GroupF.create(name=NATIONAL_DATA_SCIENTIST)
        user.groups.add(group)
        user.user_profile.current_organisation = self.organisation_1
        user.save()

        self.property = PropertyFactory.create(
            organisation=self.organisation_1,
            name='PropertyA',
            province=self.province
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

        self.spatial_data = SpatialDataModelF.create(
            property=self.property
        )
        self.spatial_data_value = SpatialDataModelValueF.create(
            spatial_data=self.spatial_data,
            context_layer_value='spatial filter test'
        )


class OwnedSpeciesTestCase(OwnedSpeciesTestMixins, TestCase):

    def test_data_table_filter_by_species_name(self) -> None:
        """Test data table filter by species name"""
        url = self.url
        value = self.owned_species[0].annualpopulationperactivity_set.first()
        data = {
            "species": "SpeciesA",
            "activity": str(value.activity_type.id),
            "reports": "Property_report"
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(len(response.data[0]["Property_report"]), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["Property_report"][0]["scientific_name"],
            "SpeciesA"
        )

    def test_data_table_filter_by_no_activity(self) -> None:
        """Test data table filter by species name"""
        url = self.url
        data = {
            "species": "SpeciesA",
            "activity": '',
            "reports": "Property_report"
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(len(response.data), 0)

    def test_filter_all_reports_by_all_activity_type(self) -> None:
        """Test data table filter by activity name"""
        url = self.url
        self.owned_species[0].annualpopulationperactivity_set.all().delete()
        self.owned_species[1].annualpopulationperactivity_set.all().delete()

        data = {
            "species": "SpeciesA",
            "activity": 'all',
            "reports": "Activity_report,Property_report,Province_report,Sampling_report,Species_report"
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # We delete 2 population per activity records, now it remains only 3
        self.assertEqual(len(response.data[0]["Activity_report"]), 3)

        # Show all property report (5)
        self.assertEqual(len(response.data[1]["Property_report"]), 5)
        # Show all sampling report (5)
        self.assertEqual(len(response.data[2]["Sampling_report"]), 5)
        # Show all species report (5)
        self.assertEqual(len(response.data[3]["Species_report"]), 5)
        # Show province report
        taxon = self.owned_species[0].taxon
        province_name = self.owned_species[0].property.province.name
        self.assertEqual(
            response.data[4]["Province_report"],
            [
                {
                    "common_name": taxon.common_name_varbatim,
                    "scientific_name": taxon.scientific_name,
                    f"total_population_{province_name}": 300,
                }
            ]
        )

    def test_data_table_filter_by_activity_type(self) -> None:
        """Test data table filter by activity type"""
        url = self.url
        value = self.owned_species[0].annualpopulationperactivity_set.first()
        data = {
            "activity": str(value.activity_type.id),
            "reports": "Property_report"
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["Property_report"][0]["scientific_name"],
            "SpeciesA"
        )

    def test_filter_by_property(self) -> None:
        """Test data table filter by property"""
        value = self.owned_species[0].annualpopulationperactivity_set.first()
        data = {
            "species": self.taxon.scientific_name,
            "property": self.property.id,
            "start_year": self.owned_species[0].annualpopulation_set.first().year,
            "end_year": self.owned_species[0].annualpopulation_set.first().year,
            "spatial_filter_values": "spatial filter test",
            "activity": str(value.activity_type.id),
            "reports": "Property_report"
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
            "species": self.taxon.scientific_name,
            "start_year": year,
            "end_year": year,
            "reports": "Species_report",
            "organisation": self.organisation_1.id,
            "property": self.property.id,
            "activity": ",".join(
                [
                    str(act_id) for act_id in ActivityType.objects.values_list('id', flat=True)
                ]
            )
        }
        url = self.url
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["Species_report"][0]["year"],
            year
        )

    def test_data_table_activity_report(self) -> None:
        """Test data table activity report"""
        year = AnnualPopulationPerActivity.objects.first().year
        value = self.owned_species[0].annualpopulationperactivity_set.first()
        url = self.url
        data = {
            "species": "SpeciesA",
            "start_year": year,
            "end_year": year,
            "reports": "Activity_report",
            "activity": str(value.activity_type.id)
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if response.data:
            self.assertEqual(next(iter(response.data[0])), "Activity_report")
        else:
            self.assertEqual(response.data, [])

    def test_activity_report_without_activity_filter(self) -> None:
        """Test data table activity report without activity"""
        year = AnnualPopulationPerActivity.objects.first().year
        url = self.url
        data = {
            "species": "SpeciesA",
            "start_year": year,
            "end_year": year,
            "reports": "Activity_report",
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if response.data:
            self.assertEqual(next(iter(response.data[0])), "Activity_report")
        else:
            self.assertEqual(response.data, [])

    def test_data_table_sampling_report(self) -> None:
        """Test data table sampling report"""
        year = self.owned_species[1].annualpopulation_set.first().year
        value = self.owned_species[1].annualpopulationperactivity_set.first()
        url = self.url
        data = {
            "species": "SpeciesA",
            "start_year": year,
            "end_year": year,
            "reports": "Sampling_report",
            "activity": str(value.activity_type.id)
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["Sampling_report"][0][
                "scientific_name"
            ],
            "SpeciesA"
        )


class NationalUserTestCase(TestCase):
    def setUp(self) -> None:
        """Setup test case"""
        taxon_rank = TaxonRank.objects.filter(
            name='Species'
        ).first()
        if not taxon_rank:
            taxon_rank = TaxonRankFactory.create(
                name='Species'
            )
        self.taxon = TaxonFactory.create(
            taxon_rank=taxon_rank,
            scientific_name='SpeciesA'
        )
        user = User.objects.create_user(
            username='testuserd',
            password='testpasswordd'
        )
        self.organisation_1 = organisationFactory.create()
        # add user 1 to organisation 1 and 3
        self.role_organisation_manager = userRoleTypeFactory.create(
            name="National data consumer",
        )
        user.user_profile.current_organisation = self.organisation_1
        user.save()

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

        self.spatial_data = SpatialDataModelF.create(
            property=self.property
        )
        self.spatial_data_value = SpatialDataModelValueF.create(
            spatial_data=self.spatial_data,
            context_layer_value='spatial filter test'
        )

    def test_national_property_report(self) -> None:
        """Test property report for national data consumer"""
        url = self.url
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_national_user_reports(self) -> None:
        """Test national data consumer reports"""
        year = self.owned_species[0].annualpopulation_set.first().year
        property = self.owned_species[0].property.id
        organisation = self.owned_species[0].property.organisation_id
        value = self.owned_species[0].annualpopulationperactivity_set.first()
        data = {
            "species": "SpeciesA",
            "property": property,
            "organisation": organisation,
            "start_year": year,
            "end_year": year,
            "reports": (
                "Activity_report,Province_report,"
                "Species_report,Property_report"
            ),
            "activity": str(value.activity_type.id),
            'spatial_filter_values': 'spatial filter test',
        }
        url = self.url
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)


class RegionalUserTestCase(TestCase):
    def setUp(self) -> None:
        """Setup test case"""
        taxon_rank = TaxonRank.objects.filter(
            name='Species'
        ).first()
        if not taxon_rank:
            taxon_rank = TaxonRankFactory.create(
                name='Species'
            )
        self.taxon = TaxonFactory.create(
            taxon_rank=taxon_rank,
            scientific_name='SpeciesA'
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
            name="Regional data consumer",
        )

        group = GroupF.create(name=REGIONAL_DATA_CONSUMER)
        user.groups.add(group)

        OrganisationInvites.objects.create(
            email=user.email,
            assigned_as=MANAGER
        )

        user.user_profile.current_organisation = self.organisation_1
        user.save()

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


    def test_regional_data_consumer(self) -> None:
        """Test data table filter by regional data consumer"""
        data = {
            "reports": "Activity_report,Species_report,Property_report",
            "activity": ",".join(
                [
                    str(act_id) for act_id in ActivityType.objects.values_list('id', flat=True)
                ]
            )
        }
        url = self.url
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)


class DataScientistTestCase(TestCase):
    def setUp(self) -> None:
        """Setup test case"""
        taxon_rank = TaxonRank.objects.filter(
            name='Species'
        ).first()
        if not taxon_rank:
            taxon_rank = TaxonRankFactory.create(
                name='Species'
            )
        self.taxon = TaxonFactory.create(
            taxon_rank=taxon_rank,
            scientific_name='SpeciesA'
        )
        user = User.objects.create_user(
                username='testuserd',
                password='testpasswordd'
            )
        self.organisation_1 = organisationFactory.create(national=True)

        organisationUserFactory.create(
            user=user,
            organisation=self.organisation_1
        )

        group = GroupF.create(name=REGIONAL_DATA_SCIENTIST)
        user.groups.add(group)
        user.user_profile.current_organisation = self.organisation_1
        user.save()

        self.role_organisation_manager = userRoleTypeFactory.create(
            name="Regional data scientist",
        )
        user.user_profile.current_organisation = self.organisation_1
        user.user_profile.user_role_type_id = self.role_organisation_manager
        user.save()

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

    def test_regional_data_scientist(self) -> None:
        """Test data table filter by regional data scientist"""
        value = self.owned_species[0].annualpopulationperactivity_set.first()
        data = {
            "reports": (
                "Species_report,Property_report"
            ),
            "activity": str(value.activity_type.id)
        }
        url = self.url
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
