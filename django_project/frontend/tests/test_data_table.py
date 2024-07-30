import base64
import csv
import os
import shutil

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from activity.models import ActivityType
from frontend.static_mapping import (
    NATIONAL_DATA_SCIENTIST,
    PROVINCIAL_DATA_SCIENTIST,
    PROVINCIAL_DATA_CONSUMER,
    NATIONAL_DATA_CONSUMER
)
from frontend.tests.model_factories import (
    SpatialDataModelF,
    SpatialDataModelValueF
)
from frontend.utils.data_table import (
    ACTIVITY_REPORT,
    SPECIES_REPORT,
    PROPERTY_REPORT,
    PROVINCE_REPORT
)
from population_data.factories import (
    AnnualPopulationF
)
from population_data.models import AnnualPopulation, AnnualPopulationPerActivity
from property.factories import PropertyFactory, ProvinceFactory
from property.models import Property
from sawps.tests.models.account_factory import GroupF
from species.factories import (
    TaxonFactory,
    TaxonRankFactory
)
from species.models import TaxonRank
from stakeholder.factories import (
    organisationFactory,
    organisationUserFactory,
    userRoleTypeFactory,
)
from stakeholder.models import OrganisationInvites, MANAGER


def get_path_from_media_url(media_url):
    data_path = media_url.replace(settings.MEDIA_URL, '')
    return os.path.join(settings.MEDIA_ROOT, data_path)


class AnnualPopulationTestMixins:

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
        self.user = User.objects.create_user(
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
            user=self.user,
            organisation=self.organisation_1
        )
        group = GroupF.create(name=NATIONAL_DATA_SCIENTIST)
        self.user.groups.add(group)
        self.user.user_profile.current_organisation = self.organisation_1
        self.user.save()

        self.property = PropertyFactory.create(
            organisation=self.organisation_1,
            name='PropertyA',
            province=self.province
        )

        self.annual_populations = AnnualPopulationF.create_batch(
            5,
            taxon=self.taxon,
            user=self.user,
            property=self.property,
            total=10,
            adult_male=4,
            adult_female=6
        )
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
        self.organisations = [self.organisation_1.id]


class AnnualPopulationTestCase(AnnualPopulationTestMixins, TestCase):

    def test_data_table_filter_by_species_name(self) -> None:
        """Test data table filter by species name"""
        url = self.url
        value = self.annual_populations[0].annualpopulationperactivity_set.first()
        data = {
            "species": "SpeciesA",
            "activity": str(value.activity_type.id),
            "reports": "Property_report",
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)])
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(len(response.data[0]["Property_report"]), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["Property_report"][0]["scientific_name"],
            "SpeciesA"
        )

    def test_data_table_filter_by_no_activity(self) -> None:
        """Test data table filter without specifying any activity.
        It will return all data.
        """
        url = self.url
        data = {
            "species": "SpeciesA",
            "activity": '',
            "reports": "Property_report",
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)])
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(len(response.data), 1)

    def test_show_all_reports(self) -> None:
        """Test showing report for a species."""
        url = self.url
        self.annual_populations[0].annualpopulationperactivity_set.all().delete()
        self.annual_populations[1].annualpopulationperactivity_set.all().delete()

        taxon = TaxonFactory.create()
        # This will not be included since the Species is not
        # the one specified in request parameter
        AnnualPopulation.objects.create(
            taxon=taxon,
            user=self.annual_populations[0].user,
            property=self.property,
            total=20,
            adult_male=8,
            adult_female=12,
            year=self.annual_populations[0].year,
            area_available_to_species=5
        )

        property_obj = PropertyFactory.create(
            organisation=self.property.organisation
        )

        # This will be included
        AnnualPopulation.objects.create(
            taxon=self.annual_populations[0].taxon,
            user=self.annual_populations[0].user,
            property=property_obj,
            total=20,
            adult_male=8,
            adult_female=12,
            year=self.annual_populations[0].year,
            area_available_to_species=10
        )

        data = {
            "species": "SpeciesA",
            "activity": '',
            "reports": "Activity_report,Property_report,Province_report,Sampling_report,Species_report",
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)])
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # We delete 2 population per activity records, now it remains only 3
        self.assertEqual(len(response.data[0]["Activity_report"]), 3)

        # Show all property report (1)
        # We only have 1 property with 5 years of data
        self.assertEqual(len(response.data[1]["Property_report"]), 6)
        for row in response.data[1]["Property_report"]:
            if row['year'] == int(self.annual_populations[0].year):
                self.assertEqual(row['area_available_to_species'], 10.0)
            else:
                self.assertEqual(row['area_available_to_species'], 10)

        # Show all sampling report (5)
        self.assertEqual(len(response.data[2]["Sampling_report"]), 6)
        # Show all species report (5)
        self.assertEqual(len(response.data[3]["Species_report"]), 6)
        # Show province report
        self.assertEqual(
            response.data[4]["Province_report"],
            [
                {
                    "year": int(self.annual_populations[4].year),
                    "common_name": self.annual_populations[-1].taxon.common_name_verbatim,
                    "scientific_name": self.annual_populations[-1].taxon.scientific_name,
                    "total_population_Western Cape": 10,
                    f"total_population_{property_obj.province.name}": 0,
                },
                {
                    "year": int(self.annual_populations[3].year),
                    "common_name": self.annual_populations[-1].taxon.common_name_verbatim,
                    "scientific_name": self.annual_populations[-1].taxon.scientific_name,
                    "total_population_Western Cape": 10,
                    f"total_population_{property_obj.province.name}": 0,
                },
                {
                    "year": int(self.annual_populations[2].year),
                    "common_name": self.annual_populations[-1].taxon.common_name_verbatim,
                    "scientific_name": self.annual_populations[-1].taxon.scientific_name,
                    "total_population_Western Cape": 10,
                    f"total_population_{property_obj.province.name}": 0,
                },
                {
                    "year": int(self.annual_populations[1].year),
                    "common_name": self.annual_populations[-1].taxon.common_name_verbatim,
                    "scientific_name": self.annual_populations[-1].taxon.scientific_name,
                    "total_population_Western Cape": 10,
                    f"total_population_{property_obj.province.name}": 0,
                },
                {
                    "year": int(self.annual_populations[0].year),
                    "common_name": self.annual_populations[-1].taxon.common_name_verbatim,
                    "scientific_name": self.annual_populations[-1].taxon.scientific_name,
                    "total_population_Western Cape": 10,
                    f"total_population_{property_obj.province.name}": 20,
                },
            ]
        )

    def test_data_table_filter_by_activity_type(self) -> None:
        """Test data table filter by activity type"""
        url = self.url
        value = self.annual_populations[0].annualpopulationperactivity_set.first()
        data = {
            "activity": str(value.activity_type.id),
            "reports": "Property_report",
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)]),
            "species": self.taxon.scientific_name
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["Property_report"][0]["scientific_name"],
            "SpeciesA"
        )

    def test_filter_by_property(self) -> None:
        """Test data table filter by property"""
        value = self.annual_populations[0].annualpopulationperactivity_set.first()
        data = {
            "species": self.taxon.scientific_name,
            "property": self.property.id,
            "start_year": self.annual_populations[0].year,
            "end_year": self.annual_populations[0].year,
            "spatial_filter_values": "spatial filter test",
            "activity": str(value.activity_type.id),
            "organisation": ','.join([str(id) for id in self.organisations]),
            "reports": "Property_report"
        }
        response = self.client.get(self.url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["Property_report"][0]["property_name"],
            "PropertyA"
        )

    def test_filter_without_property(self) -> None:
        """Test data table filter without property"""
        data = {
            "property": ''
        }
        response = self.client.get(self.url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 0,
        )

    def test_filter_by_year_and_report(self) -> None:
        """Test data table filter by year and report"""
        year = self.annual_populations[1].year
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
            int(year)
        )

    def test_data_table_activity_report(self) -> None:
        """Test data table activity report"""
        year = AnnualPopulationPerActivity.objects.first().year
        value = self.annual_populations[0].annualpopulationperactivity_set.first()
        url = self.url
        data = {
            "species": "SpeciesA",
            "start_year": year,
            "end_year": year,
            "reports": "Activity_report",
            "activity": str(value.activity_type.id),
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)])
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(next(iter(response.data[0])), "Activity_report")

    def test_data_table_sampling_report(self) -> None:
        """Test data table sampling report"""
        year = self.annual_populations[1].year
        value = self.annual_populations[1].annualpopulationperactivity_set.first()
        url = self.url
        data = {
            "species": "SpeciesA",
            "start_year": year,
            "end_year": year,
            "reports": "Sampling_report",
            "activity": str(value.activity_type.id),
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)])
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["Sampling_report"][0][
                "scientific_name"
            ],
            "SpeciesA"
        )

    def test_data_table_post(self) -> None:
        """Test data table with post request"""
        year = self.annual_populations[1].year
        value = self.annual_populations[1].annualpopulationperactivity_set.first()
        url = self.url
        data = {
            "species": "SpeciesA",
            "start_year": year,
            "end_year": year,
            "reports": "Sampling_report",
            "activity": str(value.activity_type.id),
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)])
        }
        response = self.client.post(url, data, **self.auth_headers)
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
        self.national_data_consumer_group, _ = Group.objects.get_or_create(name=NATIONAL_DATA_CONSUMER)
        user.groups.add(self.national_data_consumer_group)

        self.property = PropertyFactory.create(
            organisation=self.organisation_1,
            name='PropertyA'
        )

        self.annual_populations = AnnualPopulationF.create_batch(
            5,
            taxon=self.taxon,
            user=user,
            property=self.property,
            total=10,
            adult_male=4,
            adult_female=6
        )
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
        self.organisations = [self.organisation_1.id]

    def test_national_property_report_all_activity(self) -> None:
        """Test property report for national data consumer"""
        annual_population = AnnualPopulation.objects.create(
            taxon=self.taxon,
            property=PropertyFactory.create(),
            year=self.annual_populations[0].year,
            total=21
        )
        url = self.url
        params = {
            'activity': '',
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)]),
            "species": self.taxon.scientific_name
        }
        response = self.client.get(url, params, **self.auth_headers)
        expected_response = [
            {
                PROPERTY_REPORT: [{
                    'year': int(self.annual_populations[0].year),
                    'common_name': self.taxon.common_name_verbatim,
                    'scientific_name': self.taxon.scientific_name,
                    f'total_population_{self.property.property_type.name}_property': 10,
                    f'total_area_{self.property.property_type.name}_property': 200,
                    f'total_population_{annual_population.property.property_type.name}_property': 21,
                    f'total_area_{annual_population.property.property_type.name}_property': 200
                }]
            }
        ]
        expected_response[0][PROPERTY_REPORT].extend([{
            'year': int(self.annual_populations[i].year),
            'common_name': self.taxon.common_name_verbatim,
            'scientific_name': self.taxon.scientific_name,
            f'total_population_{self.property.property_type.name}_property': 10,
            f'total_area_{self.property.property_type.name}_property': 200,
            f'total_population_{annual_population.property.property_type.name}_property': 0,
            f'total_area_{annual_population.property.property_type.name}_property': 0
        } for i in range(1, len(self.annual_populations))])
        expected_response[0][PROPERTY_REPORT] = sorted(
            expected_response[0][PROPERTY_REPORT],
            key=lambda a: a['year'],
            reverse=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_national_activity_report_all_activity(self) -> None:
        """Test activity report for national data consumer"""
        url = self.url
        params = {
            'activity': ','.join([str(act_id) for act_id in ActivityType.objects.values_list('id', flat=True)]),
            'reports': ACTIVITY_REPORT,
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)]),
            "species": self.taxon.scientific_name
        }
        response = self.client.get(url, params, **self.auth_headers)
        expected_response = [
            {
                "Activity_report": []
            }
        ]
        for i in range(0, len(self.annual_populations)):
            activity_types = ActivityType.objects.exclude(
                name=self.annual_populations[i].annualpopulationperactivity_set.first().activity_type.name
            ).values_list('name', flat=True)
            base_dict = {
                'year': int(self.annual_populations[i].year),
                'common_name': self.taxon.common_name_verbatim,
                'scientific_name': self.taxon.scientific_name,
                f'total_population_{self.annual_populations[i].annualpopulationperactivity_set.first().activity_type.name}': 100  # noqa
            }
            additional_fields = {f"total_population_{key}": 0 for key in activity_types}
            base_dict.update(additional_fields)
            expected_response[0][ACTIVITY_REPORT].append(base_dict)
        expected_response[0][ACTIVITY_REPORT] = sorted(
            expected_response[0][ACTIVITY_REPORT],
            key=lambda a: a['year'],
            reverse=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_national_species_report_all_activity(self) -> None:
        """Test species report for national data consumer"""
        url = self.url
        params = {
            'activity': ','.join([str(act_id) for act_id in ActivityType.objects.values_list('id', flat=True)]),
            'reports': SPECIES_REPORT,
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)]),
            "species": self.taxon.scientific_name
        }
        response = self.client.get(url, params, **self.auth_headers)

        expected_response = [
            {
                SPECIES_REPORT: [{
                    'year': int(self.annual_populations[i].year),
                    'common_name': self.taxon.common_name_verbatim,
                    'scientific_name': self.taxon.scientific_name,
                    "total_property_area": 200,
                    "total_area_available": 10,
                    "total_population": 10,
                    "adult_male_total_population": 4,
                    "adult_female_total_population": 6,
                    "sub_adult_male_total_population": 10,
                    "sub_adult_female_total_population": 10,
                    "juvenile_male_total_population": 30,
                    "juvenile_female_total_population": 30,
                } for i in range(0, len(self.annual_populations))]
            }
        ]
        expected_response[0][SPECIES_REPORT] = sorted(
            expected_response[0][SPECIES_REPORT],
            key=lambda a: a['year'],
            reverse=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_national_province_report_all_activity(self) -> None:
        """Test property report for national data consumer"""
        annual_population = AnnualPopulation.objects.create(
            taxon=self.taxon,
            property=PropertyFactory.create(),
            year=self.annual_populations[0].year,
            total=21
        )
        url = self.url
        params = {
            'activity': '',
            'reports': PROVINCE_REPORT,
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)]),
            "species": self.taxon.scientific_name
        }
        response = self.client.get(url, params, **self.auth_headers)

        expected_response = [
            {
                PROVINCE_REPORT: [{
                    'year': int(self.annual_populations[0].year),
                    'common_name': self.taxon.common_name_verbatim,
                    'scientific_name': self.taxon.scientific_name,
                    f'total_population_{self.property.province.name}': 10,
                    f'total_population_{annual_population.property.province.name}': 21
                }]
            }
        ]
        expected_response[0][PROVINCE_REPORT].extend([{
            'year': int(self.annual_populations[i].year),
            'common_name': self.taxon.common_name_verbatim,
            'scientific_name': self.taxon.scientific_name,
            f'total_population_{self.property.province.name}': 10,
            f'total_population_{annual_population.property.province.name}': 0
        } for i in range(1, len(self.annual_populations))])
        expected_response[0][PROVINCE_REPORT] = sorted(
            expected_response[0][PROVINCE_REPORT],
            key=lambda a: a['year'],
            reverse=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_national_user_reports(self) -> None:
        """Test national data consumer reports"""
        year = self.annual_populations[0].year
        property = self.annual_populations[0].property.id
        organisation = self.annual_populations[0].property.organisation_id
        value = self.annual_populations[0].annualpopulationperactivity_set.first()
        data = {
            "species": "SpeciesA",
            "property": property,
            "organisation": '',
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
        self.assertEqual(len(response.data), 0)
        # test with organisation
        data = {
            "species": "SpeciesA",
            "property": property,
            "organisation": f'{str(organisation)}',
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
        self.province = ProvinceFactory.create(
            name='Limpopo'
        )
        self.organisation_1 = organisationFactory.create(
            province=self.province
        )
        # add user 1 to organisation 1 and 3
        organisationUserFactory.create(
            user=user,
            organisation=self.organisation_1
        )
        self.role_organisation_manager = userRoleTypeFactory.create(
            name="Provincial data consumer",
        )

        group = GroupF.create(name=PROVINCIAL_DATA_CONSUMER)
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

        self.annual_populations = AnnualPopulationF.create_batch(
            5,
            taxon=self.taxon,
            user=user,
            property=self.property,
            total=10,
            adult_male=4,
            adult_female=6
        )
        self.url = reverse('data-table')

        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +
            base64.b64encode(b'testuserd:testpasswordd').decode('ascii'),
        }
        self.client = Client()
        session = self.client.session
        session.save()


    def test_no_province_data(self) -> None:
        """Test data table filter by regional data consumer.
        The response would be empty since there are no Annual Population data
        for the user's organisation's province.
        """
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
        self.assertEqual(len(response.data), 0)

    def test_has_province_data(self) -> None:
        """Test data table filter by regional data consumer.
        The response would not be empty since there are Annual Population data
        for the user's organisation's province.
        """
        self.property.province = self.organisation_1.province
        self.property.save()
        data = {
            "reports": "Activity_report,Species_report,Property_report",
            "activity": ",".join(
                [
                    str(act_id) for act_id in ActivityType.objects.values_list('id', flat=True)
                ]
            ),
            "species": self.taxon.scientific_name
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

        group = GroupF.create(name=PROVINCIAL_DATA_SCIENTIST)
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

        self.annual_populations = AnnualPopulationF.create_batch(
            5,
            taxon=self.taxon,
            user=user,
            property=self.property,
            total=10,
            adult_male=4,
            adult_female=6
        )
        self.url = reverse('data-table')

        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +
            base64.b64encode(b'testuserd:testpasswordd').decode('ascii'),
        }
        self.client = Client()
        session = self.client.session
        session.save()
        self.organisations = [self.organisation_1.id]

    def test_regional_data_scientist(self) -> None:
        """Test data table filter by regional data scientist"""
        value = self.annual_populations[0].annualpopulationperactivity_set.first()
        data = {
            "reports": (
                "Species_report,Property_report"
            ),
            "activity": str(value.activity_type.id),
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)]),
            "species": self.taxon.scientific_name
        }
        url = self.url
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class DownloadDataTestCase(AnnualPopulationTestMixins, TestCase):
    """Test Case for download data"""

    def test_download_all_reports_by_all_activity_type(self) -> None:
        """Test download data table filter by activity name"""
        url = self.url
        self.annual_populations[0].annualpopulationperactivity_set.all().delete()
        self.annual_populations[1].annualpopulationperactivity_set.all().delete()

        data = {
            "file": "csv",
            "species": "SpeciesA",
            "activity": ','.join([str(act_id) for act_id in ActivityType.objects.values_list('id', flat=True)]),
            "reports": "Activity_report,Property_report,Sampling_report,Species_report",
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)])
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test if file output is zip
        self.assertIn("data_report.zip", response.data['file'])
        data_path = get_path_from_media_url(response.data['file'])
        self.assertTrue(os.path.exists(data_path))
        path = os.path.dirname(data_path)

        # check if all csv files exist in the folder
        self.assertTrue(os.path.exists(os.path.join(path, "data_report_Species_report.csv")))
        self.assertTrue(os.path.exists(os.path.join(path, "data_report_Activity_report.csv")))
        self.assertTrue(os.path.exists(os.path.join(path, "data_report_Property_report.csv")))
        self.assertTrue(os.path.exists(os.path.join(path, "data_report_Sampling_report.csv")))

        # check fields in Activity report
        activity_path = os.path.join(path, "data_report_Activity_report.csv")
        with open(activity_path, encoding='utf-8-sig') as csv_file:
            file = csv.DictReader(csv_file)
            headers = file.fieldnames
            self.assertTrue(any("_total" in header for header in headers))
            self.assertTrue(any("_adult_male" in header for header in headers))
            self.assertTrue(any("_adult_female" in header for header in headers))
            self.assertTrue(any("_juvenile_male" in header for header in headers))
            self.assertTrue(any("_juvenile_female" in header for header in headers))
            self.assertTrue("property_name" in headers)
            self.assertTrue("scientific_name" in headers)
            self.assertTrue("common_name" in headers)
            self.assertTrue("year" in headers)

    def test_download_xlsx_data_all_reports_by_all_activity_type(self) -> None:
        """Test download data table filter by activity name"""
        url = self.url

        data = {
            "file": "xlsx",
            "species": "SpeciesA",
            "activity": ','.join([str(act_id) for act_id in ActivityType.objects.values_list('id', flat=True)]),
            "reports": "Activity_report,Property_report,Sampling_report,Species_report",
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)])
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test if file output is xlsx
        self.assertIn("data_report.xlsx", response.data['file'])
        data_path = get_path_from_media_url(response.data['file'])
        self.assertTrue(os.path.exists(data_path))

    def test_download_xlsx_data_all_reports_without_activity_filter(self) -> None:
        """Test download data table filter by activity name"""
        url = self.url

        data = {
            "file": "xlsx",
            "species": "SpeciesA",
            "reports": "Activity_report,Property_report,Sampling_report,Species_report",
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)])
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test if file output is xlsx
        self.assertIn("data_report.xlsx", response.data['file'])
        data_path = get_path_from_media_url(response.data['file'])
        self.assertTrue(os.path.exists(data_path))


class DownloadDataDataConsumerTestCase(AnnualPopulationTestMixins, TestCase):
    """Test Case for download data"""

    def setUp(self):
        super().setUp()
        self.user.groups.clear()
        group = Group.objects.create(name=NATIONAL_DATA_CONSUMER)
        self.user.groups.add(group)
        self.user.save()
        self.user.user_profile.current_organisation = self.organisation_1

    def test_download_all_reports_by_all_activity_type(self) -> None:
        """Test download data table filter by activity name"""
        url = self.url
        self.annual_populations[0].annualpopulationperactivity_set.all().delete()
        self.annual_populations[1].annualpopulationperactivity_set.all().delete()

        data = {
            "file": "csv",
            "species": "SpeciesA",
            "activity": ','.join([str(act_id) for act_id in ActivityType.objects.values_list('id', flat=True)]),
            "reports": "Activity_report,Property_report,Species_report,Province_report",
            "organisation": ','.join([str(id) for id in self.organisations]),
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)])
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test if file output is zip
        self.assertIn("data_report.zip", response.data['file'])
        data_path = get_path_from_media_url(response.data['file'])
        self.assertTrue(os.path.exists(data_path))
        path = os.path.dirname(data_path)

        # check if all csv files exist in the folder
        self.assertTrue(os.path.exists(os.path.join(path, "data_report_Species_report.csv")))
        self.assertTrue(os.path.exists(os.path.join(path, "data_report_Activity_report.csv")))
        self.assertTrue(os.path.exists(os.path.join(path, "data_report_Property_report.csv")))

        # check fields in Activity report
        activity_path = os.path.join(path, "data_report_Activity_report.csv")
        with open(activity_path, encoding='utf-8-sig') as csv_file:
            file = csv.DictReader(csv_file)
            headers = file.fieldnames
            self.assertTrue(any("total_population_" in header for header in headers))
            self.assertTrue("scientific_name" in headers)
            self.assertTrue("common_name" in headers)
            self.assertTrue("year" in headers)

        activity_path = os.path.join(path, "data_report_Province_report.csv")
        with open(activity_path, encoding='utf-8-sig') as csv_file:
            file = csv.DictReader(csv_file)
            headers = file.fieldnames
            self.assertTrue(any("total_population_" in header for header in headers))
            self.assertTrue("scientific_name" in headers)
            self.assertTrue("common_name" in headers)
            self.assertTrue("year" in headers)

        activity_path = os.path.join(path, "data_report_Species_report.csv")
        with open(activity_path, encoding='utf-8-sig') as csv_file:
            file = csv.DictReader(csv_file)
            headers = file.fieldnames
            self.assertTrue("scientific_name" in headers)
            self.assertTrue("common_name" in headers)
            self.assertTrue("year" in headers)

        activity_path = os.path.join(path, "data_report_Property_report.csv")
        with open(activity_path, encoding='utf-8-sig') as csv_file:
            file = csv.DictReader(csv_file)
            headers = file.fieldnames
            self.assertTrue(any("total_population_" in header for header in headers))
            self.assertTrue("scientific_name" in headers)
            self.assertTrue("common_name" in headers)
            self.assertTrue("year" in headers)

    def test_download_xlsx_data_all_reports_by_all_activity_type(self) -> None:
        """Test download data table filter by activity name"""
        url = self.url

        data = {
            "file": "xlsx",
            "species": "SpeciesA",
            "activity": ','.join([str(act_id) for act_id in ActivityType.objects.values_list('id', flat=True)]),
            "reports": "Activity_report,Property_report,Species_report,Province_report",
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)])
        }
        response = self.client.get(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test if file output is xlsx
        self.assertIn("data_report.xlsx", response.data['file'])
        data_path = get_path_from_media_url(response.data['file'])
        self.assertTrue(os.path.exists(data_path))

    def test_download_one_report(self) -> None:
        """Test download data table with only one report"""
        url = self.url

        data = {
            "file": "csv",
            "species": "SpeciesA",
            "activity": ','.join([str(act_id) for act_id in ActivityType.objects.values_list('id', flat=True)]),
            "reports": "Species_report",
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)])
        }
        response = self.client.post(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data_report_Species_report.csv", response.data['file'])

    def test_path_not_exist(self):
        """Test download data table when file path does not exist"""

        path = os.path.join(settings.MEDIA_ROOT, "download_data")
        shutil.rmtree(path, ignore_errors=True)

        url = self.url

        data = {
            "file": "csv",
            "species": "SpeciesA",
            "activity": ','.join([str(act_id) for act_id in ActivityType.objects.values_list('id', flat=True)]),
            "reports": "Species_report",
            "property": ','.join([str(prop) for prop in Property.objects.values_list('id', flat=True)])
        }
        response = self.client.post(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data_report_Species_report.csv", response.data['file'])
