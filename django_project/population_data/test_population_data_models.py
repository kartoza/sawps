"""Test case for population data models.
"""
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase
from population_data.factories import (
    AnnualPopulationF,
    AnnualPopulationPerActivityFactory,
    CertaintyF,
    CountMethodFactory,
    OpenCloseSystemF,
    PopulationEstimateCategoryF,
    PopulationStatusF,
)
from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity,
    Certainty,
    CountMethod,
    OpenCloseSystem,
    PopulationEstimateCategory,
    PopulationStatus,
)
from species.factories import OwnedSpeciesFactory, TaxonFactory, TaxonRankFactory
from species.models import OwnedSpecies, Taxon


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


class PopulationCountTestCase(TestCase):
    """Population count test case."""
    @classmethod
    def setUpTestData(cls):
        """SetUpTestData for population count test case."""
        taxon = TaxonFactory.create(
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
            self.assertEqual(IntegrityError, raised.exception)


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

    def test_delete_population_count(self):
        """Test delete population count."""
        initial_count = AnnualPopulationPerActivity.objects.count()
        self.population_count.delete()
        with self.assertRaises(AnnualPopulationPerActivity.DoesNotExist):
            AnnualPopulationPerActivity.objects.get(pk=self.population_count.pk)
        self.assertEqual(
            AnnualPopulationPerActivity.objects.count(),
            initial_count - 1,
            msg="The count of AnnualPopulationPerActivity"
            "instances did not decrease by 1 after deletion."
        )



class TestCertainty(TestCase):
    """Test for certainty model."""

    def setUp(self) -> None:
        """setup test data"""
        self.Certainty = CertaintyF(name='name', description='text')

    def test_create_certainty(self):
        """test create certainty."""
        self.assertEqual(self.Certainty.name, 'name')
        self.assertEqual(self.Certainty.description, 'text')
        self.assertEqual(Certainty.objects.count(), 1)

    def test_update_Certainty(self):
        """test update certainty."""
        self.Certainty.name = 'Certainty'
        self.Certainty.description = 'Certainty description'
        self.Certainty.save()
        self.assertEqual(self.Certainty.name, 'Certainty')
        self.assertEqual(self.Certainty.description, 'Certainty description')

    def test_delete_certainty(self):
        """test delete certainty."""
        self.Certainty.delete()
        self.assertEqual(Certainty.objects.count(), 0)


class TestOpenCloseSystem(TestCase):
    """Test for open close system model."""

    def setUp(self) -> None:
        """setup test data"""
        self.open_close_sustem = OpenCloseSystemF(name='name')

    def test_create_open_close_system(self):
        """test create open close system."""
        self.assertEqual(self.open_close_sustem.name, 'name')
        self.assertEqual(OpenCloseSystem.objects.count(), 1)

    def test_update_open_close_system(self):
        """test update open close system."""
        self.open_close_sustem.name = 'OpenCloseSystem'
        self.open_close_sustem.save()
        self.assertEqual(self.open_close_sustem.name, 'OpenCloseSystem')

    def test_delete_open_close_system(self):
        """test delete open close system."""
        self.open_close_sustem.delete()
        self.assertEqual(OpenCloseSystem.objects.count(), 0)


class TestPopulationEstimateCategory(TestCase):
    """Test for population estimate category model."""

    def setUp(self) -> None:
        """setup test data."""
        self.population_estimate_category = PopulationEstimateCategoryF(
            name='name'
            )

    def test_create_population_estimate(self):
        """test create population estimate category."""
        self.assertEqual(self.population_estimate_category.name, 'name')
        self.assertEqual(PopulationEstimateCategory.objects.count(), 1)

    def test_update_population_estimate(self):
        """test update population estimate category."""
        self.population_estimate_category.name = 'PopulationEstimateCategory'
        self.population_estimate_category.save()
        self.assertEqual(
            self.population_estimate_category.name,
            'PopulationEstimateCategory'
        )

    def test_delete_population_estimate(self):
        """test delete population estimate category."""
        self.population_estimate_category.delete()
        self.assertEqual(PopulationEstimateCategory.objects.count(), 0)

    def test_population_estimate_name_constraint(self):
        """Test population estimate category name contraint."""
        another = PopulationEstimateCategoryF(name='Population estimate')
        self.assertEqual(PopulationEstimateCategory.objects.count(), 2)
        self.assertNotEqual(
            self.population_estimate_category.name,
            another.name
        )
        with self.assertRaises(Exception) as raised:
            PopulationEstimateCategoryF(name='name')


class TestPopulationSatatus(TestCase):
    """Test for population status model."""

    def setUp(self) -> None:
        """setup test data."""
        self.population_status = PopulationStatusF(
            name='name'
            )

    def test_create_population_status(self):
        """test create population status."""
        self.assertEqual(self.population_status.name, 'name')
        self.assertEqual(PopulationStatus.objects.count(), 1)

    def test_update_population_status(self):
        """test update population status."""
        self.population_status.name = 'PopulationSatatus'
        self.population_status.save()
        self.assertEqual(
            self.population_status.name,
            'PopulationSatatus'
        )

    def test_delete_population_status(self):
        """test delete population status."""
        self.population_status.delete()
        self.assertEqual(PopulationStatus.objects.count(), 0)

    def test_population_status_name_constraint(self):
        """Test population status name contraint."""
        another = PopulationStatusF(name='Population Status')
        self.assertEqual(PopulationStatus.objects.count(), 2)
        self.assertNotEqual(self.population_status.name, another.name)

        with self.assertRaises(Exception) as raised:
            PopulationStatusF(name='name')
