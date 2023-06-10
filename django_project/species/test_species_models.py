
from django.test import TestCase
from species.models import TaxonRank, Taxon, ManagementStatus, OwnedSpecies
from species.factories import TaxonRankFactory, ManagementStatusFactory, OwnedSpeciesFactory
from django.db.utils import IntegrityError


class ManagementStatusTestCase(TestCase):
    """Management status test case."""
    @classmethod
    def setUpTestData(cls):
        """Set up data for management status test case."""
        cls.management_status  = ManagementStatusFactory()

    def test_management_status_create(self):
        """ test management status create """
        self.assertTrue(isinstance(self.management_status, ManagementStatus))
        self.assertEqual(ManagementStatus.objects.count(), 1)
        self.assertEqual(self.management_status.name,'management status_0')

    def test_update_management_status(self):
        """Test management status update."""
        self.management_status.name = 'management status_1'
        self.management_status.save()
        self.assertEqual(ManagementStatus.objects.get(id=1).name, 'management status_1')

    
    def test_management_status_unique_name_constraint(self):
        """Test management status unique name constraint."""
        with self.assertRaises(Exception) as raised:
            ManagementStatusFactory(name='management status_1')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_management_status(self):
        """Test delete management status."""
        self.management_status.delete()
        self.assertEqual(ManagementStatus.objects.count(), 0)


class TaxonRankTestCase(TestCase):
    """Taxon rank test case."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for taxon rank test case."""
        cls.taxonRank = TaxonRankFactory()

    def test_create_taxon_rank(self):
        """Test create taxon rank."""
        self.assertTrue(isinstance(self.taxonRank, TaxonRank))
        self.assertEqual(self.taxonRank.name, 'taxon_rank_0')

    def test_update_taxon_rank(self):
        """Test update taxon rank."""
        self.taxonRank.name = 'taxon_rank_1'
        self.taxonRank.save()
        self.assertEqual(TaxonRank.objects.get(id=1).name, 'taxon_rank_1')

    def test_unique_taxon_rank_name_constraint(self):
        """Test unique taxon rank name constraint."""
        with self.assertRaises(Exception) as raised:
            TaxonRankFactory(name='taxon_rank_1')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_taxon_rank(self):
        """Test delete taxon rank."""
        self.taxonRank.delete()
        self.assertEqual(TaxonRank.objects.count(), 0)


class TaxonTestCase(TestCase):
    """Taxon model test case."""
    @classmethod
    def setUpTestData(cls):
        """Taxon model test data."""
        cls.taxonRank = TaxonRankFactory()
        cls.taxon = Taxon.objects.create(
            scientific_name='taxon_0',
            common_name_varbatim='taxon_0',
            colour_variant=False,
            taxon_rank=cls.taxonRank,
        )

    def test_create_taxon(self):
        """Test create taxon."""
        self.assertTrue(isinstance(self.taxon, Taxon))
        self.assertEqual(Taxon.objects.count(), 1)
        self.assertEqual(self.taxon.scientific_name, 'taxon_0')

    def test_update_taxon(self):
        """Test update taxon objects."""
        self.taxon.scientific_name = 'taxon_1'
        self.taxon.infraspecific_epithet = 'infra_1'
        self.taxon.save()
        self.assertEqual(Taxon.objects.get(id=1).scientific_name, 'taxon_1')
        self.assertEqual(Taxon.objects.get(id=1).infraspecific_epithet, 'infra_1')

    def test_taxon_unique_scientific_name_constraint(self):
        """Test taxon unique scientific name constraint."""
        with self.assertRaises(Exception) as raised:
            Taxon.objects.create(
                scientific_name='taxon_1',
                common_name_varbatim='taxon_0',
                colour_variant=False,
                taxon_rank=self.taxonRank,
            )
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_taxon_unique_infraspecific_epithet_constraint(self):
        """Test taxon unique infraspecific epithet constraint."""
        with self.assertRaises(Exception) as raised:
            Taxon.objects.create(
                scientific_name='taxon_0',
                common_name_varbatim='taxon_0',
                colour_variant=False,
                infraspecific_epithet='infra_1',
                taxon_rank=self.taxonRank,
            )
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_taxon_relation_to_self(self):
        """Test taxon relation to self."""
        self.taxon2 = Taxon.objects.create(
            scientific_name='taxon_1',
            common_name_varbatim='taxon_1',
            colour_variant=False,
            taxon_rank=self.taxonRank,
            parent=self.taxon,
        )
        self.assertEqual(self.taxon2.parent, self.taxon)


    def test_delete_taxon(self):
        """Test delete taxon."""
        self.taxon.delete()
        self.assertEqual(Taxon.objects.count(), 0)
        """Test delete taxon rank."""
        self.taxonRank.delete()
        self.assertEqual(TaxonRank.objects.count(), 0)


class OwnedSpeciesTestCase(TestCase):
    """Owned species test case."""
    @classmethod
    def setUpTestData(cls):
        """Set up test data for owned species test case."""
        cls.ownedSpecies = OwnedSpeciesFactory()

    def test_create_owned_species(self):
        """Test create owned species."""
        self.assertTrue(isinstance(self.ownedSpecies, OwnedSpecies))
        self.assertEqual(OwnedSpecies.objects.count(), 1)

    def test_update_owned_species(self):
        """Test update owned species."""
        self.ownedSpecies.management_status = 'management_status_1'
        self.ownedSpecies.save()
        self.assertEqual(OwnedSpecies.objects.get(id=1).management_status.name, 'management_status_1')

    def test_delete_owned_species(self):
        """Test delete owned species."""
        self.ownedSpecies.delete()
        self.assertEqual(OwnedSpecies.objects.count(), 0)