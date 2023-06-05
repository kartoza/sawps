from django.test import TestCase
from species.models import ManagementStatus
from species.factories import ManagementStatusFactory
from django.db.utils import IntegrityError

class ManagementStatusTestCase(TestCase):
    """ management status test case """
    @classmethod
    def setUpTestData(cls):
        """ set up data for management status test case """
        cls.management_status  = ManagementStatusFactory()

    def test_management_status_create(self):
        """ test management status create """
        self.assertTrue(isinstance(self.management_status, ManagementStatus))
        self.assertEqual(ManagementStatus.objects.count(), 1)
        self.assertEqual(self.management_status.name,'management status_0')

    def test_update_management_status(self):
        """ test management status update """
        self.management_status.name = 'management status_1'
        self.management_status.save()
        self.assertEqual(ManagementStatus.objects.get(id=1), 'management status_1')

    
    def test_management_status_unique_name_constraint(self):
        """ test management status unique name constraint """
        with self.assertRaises(Exception) as raised:
            ManagementStatusFactory(name='management status_1')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_management_status(self):
        """ test delete management status """
        self.management_status.delete()
        self.assertEqual(ManagementStatus.objects.count(), 0)