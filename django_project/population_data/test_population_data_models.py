from django.test import TestCase
from population_data.models import CountMethod
from population_data.factories import CountMethodFactory
from django.db.utils import IntegrityError


class CountMethodTestCase(TestCase):
    """count method test case"""

    @classmethod
    def setUpTestData(cls):
        """setupTestData for count method test case"""
        cls.count_method = CountMethodFactory()

    def test_create_count_method(self):
        """test create count method"""
        self.assertTrue(isinstance(self.count_method, CountMethod))
        self.assertEqual(CountMethod.objects.count(), 1)
        self.assertEqual(self.count_method.name, 'count method-1')

    def test_update_count_method(self):
        """test update count method"""
        self.count_method.name = 'count method-2'
        self.count_method.save()
        self.assertEqual(CountMethod.objects.get(id=1).name, 'count method-2')

    def test_count_method_unique_name_constraint(self):
        """test count method unique name constraint"""
        with self.assertRaises(Exception) as raised:
            CountMethodFactory(name='count method-2')
            self.assertEqual(raised.exception, IntegrityError)

    def test_delete_count_method(self):
        """test delete count method"""
        self.count_method.delete()
        self.assertEqual(CountMethod.objects.count(), 0)