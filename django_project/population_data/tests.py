from django.test import TestCase
from population_data.models import Month
from population_data.factories import MonthFactory
from django.db.utils import IntegrityError

class MonthTestCase(TestCase):
    """ month test case """
    @classmethod
    def setUpTestData(cls):
        cls.month  = MonthFactory()
    
    def test_create_month(self):
        """ test create a month """
        self.assertTrue(isinstance(self.month,Month))
        self.assertEqual(Month.objects.count(),1)
        self.assertEqual(self.month.name, "month-0")

    def test_update_month(self):
        """ update month """
        self.month.name = 'month-1'
        self.month.save()
        self.assertEqual(Month.objects.get(id=1).name, 'month-1')

    def test_month_unique_name_constraint(self):
        """ test month unique name constraint """
        with self.assertRaises(Exception) as raised:
            MonthFactory(name='month-1')
            self.assertEqual(raised.exception, IntegrityError)

    def test_month_unique_sorid_constraint(self):
        """ test month unique sorid constraint """
        with self.assertRaises(Exception) as raised:
            MonthFactory(sorid=0)
            self.assertEqual(raised.exception, IntegrityError)
    
    def test_delete_month(self):
        """ test delete month """
        self.month.delete()
        self.assertEqual(Month.objects.count(),0)