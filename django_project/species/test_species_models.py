
from django.test import TestCase
from species.models import TaxonRank, Taxon
from species.factories import TaxonRankFactory
from django.db.utils import IntegrityError


class TaxonRankTestCase(TestCase):
    """taxon rank test case"""

    @classmethod
    def setUpTestData(cls):
        """set up test data for taxon rank test case"""
        cls.taxonRank = TaxonRankFactory()

    def test_create_taxon_rank(self):
        """test create taxon rank"""
        self.assertTrue(isinstance(self.taxonRank, TaxonRank))
        self.assertEqual(self.taxonRank.name, 'taxon_rank_0')

    def test_update_taxon_rank(self):
        """test update taxon rank"""
        self.taxonRank.name = 'taxon_rank_1'
        self.taxonRank.save()
        self.assertEqual(TaxonRank.objects.get(id=1).name, 'taxon_rank_1')

    def test_taxon_rank_unique_name_constraint(self):
        """test taxon unique rank name constraint"""
        with self.assertRaises(Exception) as raised:
            TaxonRankFactory(name='taxon_rank_1')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_taxon_rank(self):
        """test delete taxon rank"""
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