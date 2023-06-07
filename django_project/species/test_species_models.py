from django.test import TestCase
from species.models import ManagementStatus, TaxonRank
from species.factories import ManagementStatusFactory, TaxonRankFactory
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
