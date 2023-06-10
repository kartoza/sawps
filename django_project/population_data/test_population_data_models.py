from django.test import TestCase
from population_data.models import CountMethod, Month, NatureOfPopulation, PopulationCount, PopulationCountPerActivity
from population_data.factories import CountMethodFactory, MonthFactory, NatureOfPopulationFactory, PopulationCountFactory, PopulationCountPerActivityFactory
from species.models import Taxon, OwnedSpecies
from django.contrib.auth.models import User
from species.factories import OwnedSpeciesFactory, TaxonRankFactory
from django.db.utils import IntegrityError


class CountMethodTestCase(TestCase):
    """Count method test case."""

    @classmethod
    def setUpTestData(cls):
        """SetupTestData for count method test case."""
        cls.count_method = CountMethodFactory()

    def test_create_count_method(self):
        """Test create count method."""
        self.assertTrue(isinstance(self.count_method, CountMethod))
        self.assertEqual(CountMethod.objects.count(), 1)
        self.assertEqual(self.count_method.name, 'count method-1')

    def test_update_count_method(self):
        """Test update count method."""
        self.count_method.name = 'count method-2'
        self.count_method.save()
        self.assertEqual(CountMethod.objects.get(id=self.count_method.id).name, 'count method-2')

    def test_count_method_unique_name_constraint(self):
        """Test count method unique name constraint."""
        with self.assertRaises(Exception) as raised:
            CountMethodFactory(name='count method-2')
            self.assertEqual(raised.exception, IntegrityError)

    def test_delete_count_method(self):
        """Test delete count method."""
        self.count_method.delete()
        self.assertEqual(CountMethod.objects.count(), 0)


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
        self.assertEqual(Month.objects.get(id=self.month.id).name, 'month-1')

    def test_month_unique_name_constraint(self):
        """Test month unique name constraint."""
        with self.assertRaises(Exception) as raised:
            MonthFactory(name='month-1')
            self.assertEqual(raised.exception, IntegrityError)

    def test_month_unique_sort_order_constraint(self):
        """Test month unique sort_order constraint."""
        with self.assertRaises(Exception) as raised:
            MonthFactory(sort_order=0)
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
            NatureOfPopulation.objects.get(id=self.nature_of_population.id).name,
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


class PopulationCountTestCase(TestCase):
    """Population count test case."""
    @classmethod
    def setUpTestData(cls):
        """SetUpTestData for population count test case."""
        taxon = Taxon.objects.create(
            scientific_name='taxon_0',
            common_name_varbatim='taxon_0',
            colour_variant=False,
            taxon_rank=TaxonRankFactory(),
        )
        user = User.objects.create_user(username='testuser', password='12345')        
        OwnedSpeciesFactory(taxon=taxon, user=user)
        cls.population_count = PopulationCountFactory(owned_species=OwnedSpecies.objects.all())
    
    def test_create_population_count(self):
        """Test create population count."""
        self.assertTrue(
            isinstance(self.population_count, PopulationCount)
        )
        self.assertEqual(PopulationCount.objects.count(), 1)


    def test_update_population_count(self):
        """Test update population count."""
        self.population_count.total = 100
        self.population_count.save()
        self.assertEqual(
            PopulationCount.objects.get(year=self.population_count.year).total, 100
        )

    def test_delete_population_count(self):
        """Test delete population count."""
        self.population_count.delete()
        self.assertEqual(PopulationCount.objects.count(), 0)


class PopulationCountPerActivityTestCase(TestCase):
    """Population count test case."""
    @classmethod
    def setUpTestData(cls):
        """SetUpTestData for population count test case."""
        taxon = Taxon.objects.create(
            scientific_name='taxon_0',
            common_name_varbatim='taxon_0',
            colour_variant=False,
            taxon_rank=TaxonRankFactory(),
        )
        user = User.objects.create_user(username='testuser', password='12345')        
        OwnedSpeciesFactory(taxon=taxon, user=user)
        cls.population_count = PopulationCountPerActivityFactory(owned_species=OwnedSpecies.objects.all())
    
    def test_create_population_count(self):
        """Test create population count."""
        self.assertTrue(
            isinstance(self.population_count, PopulationCountPerActivity)
        )
        self.assertEqual(PopulationCountPerActivity.objects.count(), 1)


    def test_update_population_count(self):
        """Test update population count."""
        self.population_count.total = 100
        self.population_count.save()
        self.assertEqual(
            PopulationCountPerActivity.objects.get(year=self.population_count.year).total, 100
        )

    def test_delete_population_count(self):
        """Test delete population count."""
        self.population_count.delete()
        self.assertEqual(PopulationCountPerActivity.objects.count(), 0)
