from django.test import TestCase
from occurrence.models import OrganismQuantityType
from occurrence.factories import OrganismQuantityTypeFactory
from django.db.utils import IntegrityError


class OrganismQuantityTypeTestCase(TestCase):
    """organism quantity type test case"""

    @classmethod
    def setUpTestData(cls):
        """set up test data"""
        cls.quantityType = OrganismQuantityTypeFactory()

    def test_create_quantity_type(self):
        """test create organism quantity type"""
        self.assertTrue(isinstance(self.quantityType, OrganismQuantityType))
        self.assertEqual(OrganismQuantityType.objects.count(), 1)
        self.assertEqual(self.quantityType.name, "organism_quantity_type_0")

    def test_update_quantity_type(self):
        """test update quantity type"""
        self.quantityType.name = "organism_quantity_type_1"
        self.quantityType.save()
        self.assertEqual(
            OrganismQuantityType.objects.get(id=1).name,
            "organism_quantity_type_1",
        )

    def test_quantity_type_unique_name(self):
        """test unique names of quantity types"""
        with self.assertRaises(Exception) as raised:
            OrganismQuantityTypeFactory(name="organism_quantity_type_1")
            self.assertEqual(raised.exception, IntegrityError)

    def test_quantity_type_unique_sort_id(self):
        """test unique sort ids of quantity types"""
        with self.assertRaises(Exception) as raised:
            OrganismQuantityTypeFactory(sort_id=0)
            self.assertEqual(raised.exception, IntegrityError)

    def test_delete_quantity_type(self):
        """test delete quantity type"""
        self.quantityType.delete()
        self.assertEqual(OrganismQuantityType.objects.count(), 0)
