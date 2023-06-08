from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from population_data.models import Month, NatureOfPopulation
from population_data.factories import MonthFactory, NatureOfPopulationFactory
from django.db.utils import IntegrityError


class MonthTestCase(TestCase):
    """Month test case."""

    @classmethod
    def setUpTestData(cls):
        cls.month = MonthFactory()

    def test_create_month(self):
        """Test create a month."""
        self.assertTrue(isinstance(self.month, Month))
        self.assertEqual(Month.objects.count(), 1)
        self.assertEqual(self.month.name, 'month-0')

    def test_update_month(self):
        """Update month."""
        self.month.name = 'month-1'
        self.month.save()
        self.assertEqual(Month.objects.get(id=1).name, 'month-1')

    def test_month_unique_name_constraint(self):
        """Test month unique name constraint."""
        with self.assertRaises(Exception) as raised:
            MonthFactory(name='month-1')
            self.assertEqual(raised.exception, IntegrityError)

    def test_month_unique_sorid_constraint(self):
        """Test month unique sorid constraint."""
        with self.assertRaises(Exception) as raised:
            MonthFactory(sorid=0)
            self.assertEqual(raised.exception, IntegrityError)

    def test_delete_month(self):
        """Test delete month."""
        self.month.delete()
        self.assertEqual(Month.objects.count(), 0)


class NatureOfPopulationTestCase(TestCase):
    """Nature of population test case."""

    @classmethod
    def setUpTestData(cls):
        """SetUpTestData for nature of population test case."""
        cls.nature_of_population = NatureOfPopulationFactory()

    def test_create_nature_of_population(self):
        """Test create nature of population."""
        self.assertTrue(
            isinstance(self.nature_of_population, NatureOfPopulation)
        )
        self.assertEqual(NatureOfPopulation.objects.count(), 1)
        self.assertEqual(
            self.nature_of_population.name, 'nature of population-0'
        )

    def test_update_nature_of_population(self):
        """Test update nature of population."""
        self.nature_of_population.name = 'nature of population-1'
        self.nature_of_population.save()
        self.assertEqual(
            NatureOfPopulation.objects.get(id=1).name,
            'nature of population-1',
        )

    def test_nature_of_population_unique_name_constraint(self):
        """Test nature of population unique name constraint."""
        with self.assertRaises(Exception) as raised:
            NatureOfPopulationFactory(name='nature of population-1')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_nature_of_population(self):
        """Test delete nature of population."""
        self.nature_of_population.delete()
        self.assertEqual(NatureOfPopulation.objects.count(), 0)
