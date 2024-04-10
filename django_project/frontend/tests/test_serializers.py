from django.test import TestCase

from frontend.serializers.property import PropertySerializer
from frontend.serializers.report import (
    SamplingReportSerializer,
    PropertyReportSerializer,
    SpeciesReportSerializer,
    ActivityReportSerializer
)
from frontend.tests.test_data_table import AnnualPopulationTestMixins
from population_data.models import (
    AnnualPopulation
)
from property.factories import PropertyFactory
from frontend.tests.model_factories import UserF


class TestReportSerializer(AnnualPopulationTestMixins, TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.annual_population: AnnualPopulation = AnnualPopulation.objects.create(
            user=self.annual_populations[0].user,
            taxon=self.annual_populations[0].taxon,
            property=self.annual_populations[0].property,
            area_available_to_species=self.annual_populations[0].area_available_to_species,
            year=2021, total=30,
            adult_male=10, adult_female=10
        )
        self.superuser = UserF.create(is_superuser=True)

    def test_species_report_serializer(self):
        annual_population = AnnualPopulation.objects.first()
        serializer = SpeciesReportSerializer(annual_population)
        expected_value = {
            "property_name": self.property.name,
            "property_short_code": self.property.short_code,
            "organisation_name": self.organisation_1.name,
            "organisation_short_code": self.organisation_1.short_code,
            "scientific_name": self.taxon.scientific_name,
            "common_name": self.taxon.common_name_verbatim,
            "year": annual_population.year,
            "group": None,
            "total": annual_population.total,
            "adult_male": annual_population.adult_male,
            "adult_female": annual_population.adult_female,
            "juvenile_male": annual_population.juvenile_male,
            "juvenile_female": annual_population.juvenile_female,
            "sub_adult_male": annual_population.sub_adult_male,
            "sub_adult_female": annual_population.sub_adult_female,
            "property_id": self.property.id,
            "upload_id": annual_population.id,
            "is_editable": False
        }
        self.assertEqual(
            serializer.data,
            expected_value
        )
        other_user = UserF.create()
        serializer = SpeciesReportSerializer(
            annual_population,
            context={
                'user': other_user
            }
        )
        self.assertEqual(
            serializer.data,
            expected_value
        )
        # test with superuser
        serializer = SpeciesReportSerializer(
            annual_population,
            context={
                'user': self.superuser
            }
        )
        expected_value['is_editable'] = True
        self.assertEqual(
            serializer.data,
            expected_value
        )
        serializer = SpeciesReportSerializer(
            annual_population,
            context={
                'user': self.annual_populations[0].user
            }
        )
        expected_value['is_editable'] = True
        self.assertEqual(
            serializer.data,
            expected_value
        )
        # test with manager
        serializer = SpeciesReportSerializer(
            annual_population,
            context={
                'user': other_user,
                'managed_ids': [self.organisation_1.id]
            }
        )
        expected_value['is_editable'] = True
        self.assertEqual(
            serializer.data,
            expected_value
        )

    def test_property_report_serializer(self):
        serializer = PropertyReportSerializer(self.annual_population)
        expected_value = {
            "property_name": self.annual_population.property.name,
            "property_short_code": self.annual_population.property.short_code,
            "organisation_name": self.annual_population.property.organisation.name,
            "organisation_short_code": self.annual_population.property.organisation.short_code,
            "scientific_name": self.annual_population.taxon.scientific_name,
            "common_name": self.annual_population.taxon.common_name_verbatim,
            "owner": "",
            "owner_email": self.annual_population.property.owner_email,
            "property_type": self.annual_population.property.property_type.name,
            "province": self.annual_population.property.province.name,
            "property_size_ha": 200,
            "area_available_to_species": 10.0,
            "open_close_systems": "",
            "year": self.annual_population.year
        }

        self.assertEqual(
            serializer.data,
            expected_value
        )

    def test_sampling_report_serializer(self):
        annual_population = AnnualPopulation.objects.first()
        serializer = SamplingReportSerializer(annual_population)
        expected_value = {
            "property_name": self.property.name,
            "property_short_code": self.property.short_code,
            "organisation_name": self.organisation_1.name,
            "organisation_short_code": self.organisation_1.short_code,
            "year": annual_population.year,
            "scientific_name": self.taxon.scientific_name,
            "common_name": self.taxon.common_name_verbatim,
            "population_status": "",
            "population_estimate_category": "",
            "survey_method": "",
            "sampling_effort_coverage": "",
            "population_estimate_certainty": None,
        }

        self.assertEqual(
            serializer.data,
            expected_value
        )


class TestPropertySerializer(TestCase):
    def setUp(self) -> None:
        self.property = PropertyFactory.create()

    def test_serializer(self):
        serializer = PropertySerializer(self.property)
        expected_value = [
            'id', 'name', 'owner', 'owner_email', 'property_type', 'property_type_id',
            'province', 'province_id', 'open', 'open_id', 'size', 'organisation',
            'organisation_id', 'short_code', 'boundary_source'
        ]
        self.assertEqual(
            sorted(list(serializer.data.keys())),
            sorted(expected_value)
        )


class TestActivityReportSerializer(TestCase):

    def test_activity_not_specified(self):
        with self.assertRaises(ValueError):
            ActivityReportSerializer(
                [],
                many=True
            )
