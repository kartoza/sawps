
from django.test import TestCase
from species.models import TaxonRank
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

    def test_unique_taxon_rank_name_constraint(self):
        """test unique taxon rank name constraint"""
        with self.assertRaises(Exception) as raised:
            TaxonRankFactory(name='taxon_rank_1')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_taxon_rank(self):
        """test delete taxon rank"""
        self.taxonRank.delete()
        self.assertEqual(TaxonRank.objects.count(), 0)
