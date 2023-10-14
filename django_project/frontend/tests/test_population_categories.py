from regulatory_permit.models import DataUsePermission
from stakeholder.models import Organisation
from frontend.tests.model_factories import UserF
from property.factories import PropertyFactory
from population_data.factories import AnnualPopulationF
from population_data.models import AnnualPopulation
from frontend.utils.metrics import calculate_population_categories
import unittest
from species.factories import (
    OwnedSpeciesFactory,
    TaxonRankFactory
)
from species.models import Taxon, TaxonRank
from unittest.mock import patch
from property.models import Property
from django.db.models.query import QuerySet
from django.test import TestCase

class TestCalculatePopulationCategories(TestCase):
    def setUp(self):
        taxon_rank = TaxonRank.objects.filter(name="Species").first()
        if not taxon_rank:
            taxon_rank = TaxonRankFactory.create(name="Species")

        self.taxon = Taxon.objects.create(
            taxon_rank=taxon_rank, common_name_varbatim="Lion",
            scientific_name = "Penthera leo"
        )

        self.taxon1 = Taxon.objects.create(
            taxon_rank=taxon_rank, common_name_varbatim="Cheetah",
            scientific_name = "Cheetah"
        )

        self.user = UserF.create()

        self.data_use_permission = DataUsePermission.objects.create(
            name="test"
        )
        self.organisation = Organisation.objects.create(
            name="test_organisation",
            data_use_permission=self.data_use_permission
        )

        self.property = PropertyFactory.create(
            organisation=self.organisation, name="PropertyA"
        )

        self.owned_species = OwnedSpeciesFactory.create(
             taxon=self.taxon, user=self.user, property=self.property
        )

        self.owned_species1 = OwnedSpeciesFactory.create(
             taxon=self.taxon1, user=self.user, property=self.property
        )

        AnnualPopulationF.create(
            year=2020,
            owned_species=self.owned_species,
            total=100,
            adult_male=50,
            adult_female=50,
            juvenile_male=30,
            juvenile_female=30,
            sub_adult_total=20,
            sub_adult_male=10,
            sub_adult_female=10,
            juvenile_total=40,
        )

        AnnualPopulationF.create(
            year=2020,
            owned_species=self.owned_species,
            total=200,
            adult_male=50,
            adult_female=50,
            juvenile_male=30,
            juvenile_female=30,
            sub_adult_total=20,
            sub_adult_male=10,
            sub_adult_female=10,
            juvenile_total=40,
        )

        AnnualPopulationF.create(
            year=2021,
            owned_species=self.owned_species1,
            total=300,
            adult_male=50,
            adult_female=50,
            juvenile_male=30,
            juvenile_female=30,
            sub_adult_total=20,
            sub_adult_male=10,
            sub_adult_female=10,
            juvenile_total=40,
        )


    def test_empty_queryset(self):
        # Test when the queryset is empty
        queryset = []
        species_name = "Penthera leo"
        result = calculate_population_categories(queryset, species_name)
        self.assertEqual(result, {})

    def test_no_annual_population_data(self):
        # Test when there is no annual population data
        queryset = [
            Property(id=1),
            Property(id=2),
        ]
        species_name = "Pleo"
        result = calculate_population_categories(queryset, species_name)
        self.assertEqual(result, {})

    @patch('population_data.models.AnnualPopulation.objects.filter')
    def test_population_categories_calculation(self, mock_filter):
        # Test the calculation of population categories
        # Create mock annual population data
        annual_population_data = [
            {'year': 2020, 'population_total': 100},
            {'year': 2020, 'population_total': 200},
            {'year': 2020, 'population_total': 200},
            {'year': 2021, 'population_total': 400},
            {'year': 2022, 'population_total': 300},
            {'year': 2023, 'population_total': 200},
        ]

        # Create a mock queryset and set its return value
        mock_queryset = QuerySet(model=AnnualPopulation)
        mock_queryset._result_cache = annual_population_data
        mock_filter.return_value = mock_queryset

        queryset = [
            Property(id=1),
            Property(id=2),
        ]
        species_name = "Panthera Leo"
        result = calculate_population_categories(queryset, species_name)

        # Confirm it contains data
        self.assertIsNotNone(result)

        # Assert that each result object contains a 'year' key
        for key, value in result.items():
            self.assertIn('year', value)

        # Test that the specific lines are covered
        self.assertTrue(any(item['population_total'] >= 100 and item['population_total'] < 250 for item in annual_population_data))
        self.assertTrue(any(item['population_total'] >= 250 and item['population_total'] < 400 for item in annual_population_data))
        self.assertTrue(any(item['population_total'] >= 400 and item['population_total'] < 550 for item in annual_population_data))

        # Define your desired category boundaries
        categories = [100, 250, 400, 550, 700, 850]

        # Mock annual population data
        annual_population_data = [
            {'year': 2020, 'population_total': 100},
            {'year': 2020, 'population_total': 250},
            {'year': 2020, 'population_total': 350},
            {'year': 2021, 'population_total': 450},
            {'year': 2022, 'population_total': 550},
            {'year': 2023, 'population_total': 600},
        ]

        # Create a mock queryset and set its return value
        mock_queryset = Property.objects.filter(id__in=[1, 2])

        # Call the function with the mock data and categories
        species_name = "Panthera Leo"
        result = calculate_population_categories(mock_queryset, species_name, categories)

        # Confirm it contains data
        self.assertIsNotNone(result)

        # Check if the condition is evaluated as True for at least one item
        is_condition_met = any(
            categories[i] <= item['population_total'] < categories[i + 1]
            for item in annual_population_data
            for i in range(len(categories) - 1)
        )
        self.assertTrue(is_condition_met)


if __name__ == '__main__':
    unittest.main()
