from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from population_data.models import NatureOfPopulation
from population_data.factories import NatureOfPopulationFactory
from django.db.utils import IntegrityError


class NatureOfPopulationTestCase(TestCase):
    """nature of population test case"""

    @classmethod
    def setUpTestData(cls):
        """setUpTestData for nature of population test case"""
        cls.nature_of_population = NatureOfPopulationFactory()

    def test_create_nature_of_population(self):
        """test create nature of population"""
        self.assertTrue(
            isinstance(self.nature_of_population, NatureOfPopulation)
        )
        self.assertEqual(NatureOfPopulation.objects.count(), 1)
        self.assertEqual(
            self.nature_of_population.name, 'nature of population-0'
        )

    def test_update_nature_of_population(self):
        """test update nature of population"""
        self.nature_of_population.name = 'nature of population-1'
        self.nature_of_population.save()
        self.assertEqual(
            NatureOfPopulation.objects.get(id=1).name,
            'nature of population-1',
        )

    def test_nature_of_population_unique_name_constraint(self):
        """test nature of population unique name constraint"""
        with self.assertRaises(Exception) as raised:
            NatureOfPopulationFactory(name='nature of population-1')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_nature_of_population(self):
        """test delete nature of population"""
        self.nature_of_population.delete()
        self.assertEqual(NatureOfPopulation.objects.count(), 0)