import unittest
from django.http import HttpRequest
from frontend.serializers.metrics import TotalCountPerPopulationEstimateSerializer
from django.test import TestCase

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

if __name__ == "__main__":
    unittest.main()
