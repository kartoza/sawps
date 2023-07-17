from django.test import TestCase
from population_data.models import (
    CountMethod, 
    Month, 
    NatureOfPopulation, 
    AnnualPopulation, 
    AnnualPopulationPerActivity,
    Certainty,
    OpenCloseSystem
)
from population_data.factories import (
    CountMethodFactory, 
    MonthFactory, 
    NatureOfPopulationFactory, 
    AnnualPopulationF, 
    AnnualPopulationPerActivityFactory,
    CertaintyF,
    OpenCloseSystemF
)
from species.models import Taxon, OwnedSpecies
from django.contrib.auth.models import User
from species.factories import OwnedSpeciesFactory, TaxonRankFactory
from django.db.utils import IntegrityError


class CountMethodTestCase(TestCase):
    """Count method test case."""

    @classmethod
    def setUpTestData(cls):
        """SetupTestData for count method test case."""
        cls.count_method = CountMethodFactory(
            name='count method-1'
        )

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
        cls.month = MonthFactory(
            name='month-0'
        )

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
        cls.nature_of_population = NatureOfPopulationFactory(
            name='nature of population-0'
        )

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
        owned_species = OwnedSpeciesFactory(taxon=taxon, user=user)
        cls.population_count = AnnualPopulationF(
            owned_species=owned_species,
            total = 120,
            adult_male=19,
            adult_female=100
        )
    
    def test_create_population_count(self):
        """Test create population count."""
        self.assertTrue(
            isinstance(self.population_count, AnnualPopulation)
        )
        self.assertTrue(
            AnnualPopulation.objects.filter(
                id=self.population_count.id
            ).exists()
        )


    def test_update_population_count(self):
        """Test update population count."""
        self.population_count.total = 125
        self.population_count.save()
        self.assertEqual(
            AnnualPopulation.objects.get(year=self.population_count.year).total, 125
        )

    def test_year_ownedspecies_fields_unique_toghter_constraint(self):
        """Test both year and ownedspecis are unique togther."""
        with self.assertRaises(Exception) as raised:
            AnnualPopulationF(
                owned_species=self.population_count.owned_species,
                year=self.population_count.year,
            )
            self.assertEqual(IntegrityError, type(raised.exception))
    

    def test_delete_population_count(self):
        """Test delete population count."""
        self.population_count.delete()
        self.assertFalse(
            AnnualPopulation.objects.filter(id=self.population_count.id).exists()
        )

    def test_annual_population_total_constraint(self):
        """Test update population count."""
        self.population_count.total = 110
        with self.assertRaises(Exception) as raised:
            self.population_count.save()
            self.assertEqual(raised.exception, IntegrityError)
        



class AnnualPopulationPerActivityTestCase(TestCase):
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
        owned_species = OwnedSpeciesFactory(taxon=taxon, user=user)
        cls.population_count = AnnualPopulationPerActivityFactory(owned_species=owned_species)
    
    def test_create_population_count(self):
        """Test create population count."""
        self.assertTrue(
            isinstance(self.population_count, AnnualPopulationPerActivity)
        )
        self.assertTrue(
            AnnualPopulationPerActivity.objects.filter(
                id=self.population_count.id
            ).exists()
        )


    def test_update_population_count(self):
        """Test update population count."""
        self.population_count.total = 100
        self.population_count.save()
        self.assertEqual(
            AnnualPopulationPerActivity.objects.get(year=self.population_count.year).total, 100
        )

    def test_year_ownedspecies_activity_type_fields_unique_toghter_constraint(self):
        """Test year, ownedspecies and activity_type are unique togther."""
        with self.assertRaises(Exception) as raised:
            AnnualPopulationPerActivityFactory(
                owned_species=self.population_count.owned_species,
                year=self.population_count.year,
                activity_type=self.population_count.activity_type,
            )
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_population_count(self):
        """Test delete population count."""
        self.population_count.delete()
        self.assertEqual(AnnualPopulationPerActivity.objects.count(), 0)


class TestCertainty(TestCase):
    """Test for certainty model"""

    def setUp(self) -> None:
        """setup test data"""
        self.Certainty = CertaintyF(name='name', description='text')

    def test_create_certainty(self):
        """test create certainty"""
        self.assertEqual(self.Certainty.name, 'name')
        self.assertEqual(self.Certainty.description, 'text')
        self.assertEqual(Certainty.objects.count(), 1)

    def test_update_Certainty(self):
        """test update certainty"""
        self.Certainty.name = 'Certainty'
        self.Certainty.description = 'Certainty description'
        self.Certainty.save()
        self.assertEqual(self.Certainty.name, 'Certainty')
        self.assertEqual(self.Certainty.description, 'Certainty description')

    def test_delete_certainty(self):
        """test delete certainty"""
        self.Certainty.delete()
        self.assertEqual(Certainty.objects.count(), 0)


class TestOpenCloseSystem(TestCase):
    """Test for open close system model"""

    def setUp(self) -> None:
        """setup test data"""
        self.open_close_sustem = OpenCloseSystemF(name='name')

    def test_create_open_close_system(self):
        """test create pen close system"""
        self.assertEqual(self.open_close_sustem.name, 'name')
        self.assertEqual(OpenCloseSystem.objects.count(), 1)

    def test_update_open_close_system(self):
        """test update pen close system"""
        self.open_close_sustem.name = 'OpenCloseSystem'
        self.open_close_sustem.save()
        self.assertEqual(self.open_close_sustem.name, 'OpenCloseSystem')

    def test_delete_open_close_system(self):
        """test delete pen close system"""
        self.open_close_sustem.delete()
        self.assertEqual(OpenCloseSystem.objects.count(), 0)
