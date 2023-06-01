from django.test import TestCase
import property.models as PropertyModels
from property.factories import PropertyTypeFactory
from django.db.utils import IntegrityError


class PropertyTypeTest(TestCase):
    """propert type test case"""

    @classmethod
    def setUpTestData(cls):
        cls.property_type = PropertyTypeFactory()

    def test_create_property_type(self):
        """test creating a new property type"""
        self.assertTrue(
            isinstance(self.property_type, PropertyModels.PropertyType)
        )
        self.assertEqual(PropertyModels.PropertyType.objects.count(), 1)
        self.assertEqual(self.property_type.name, 'PropertyType 0')

    def test_update_property_type(self):
        """test updating a property type"""
        self.property_type.name = 'PropertyType 2'
        self.property_type.save()
        self.assertEqual(
            PropertyModels.PropertyType.objects.get(id=1).name,
            'PropertyType 2',
        )

    def test_property_type_unique_name_constraint(self):
        """test property type unique name constraint"""
        with self.assertRaises(Exception) as raised:
            PropertyTypeFactory(name='PropertyType 2')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_property_type(self):
        """test deleting a property type"""
        self.property_type.delete()
        self.assertEqual(PropertyModels.PropertyType.objects.count(), 0)
