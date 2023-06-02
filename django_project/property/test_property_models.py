from django.test import TestCase
import property.models as PropertyModels
import property.factories as PropertyFactories
from django.db.utils import IntegrityError


class PropertyTypeTest(TestCase):
    """propert type test case"""

    @classmethod
    def setUpTestData(cls):
        cls.property_type = PropertyFactories.PropertyTypeFactory()

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
            PropertyFactories.PropertyTypeFactory(name='PropertyType 2')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_property_type(self):
        """test deleting a property type"""
        self.property_type.delete()
        self.assertEqual(PropertyModels.PropertyType.objects.count(), 0)


class ProvinceTestCase(TestCase):
    """province test case"""

    @classmethod
    def setUpTestData(cls):
        cls.province = PropertyFactories.ProvinceFactory()

    def test_create_province(self):
        'test create a province'
        self.assertTrue(isinstance(self.province, PropertyModels.Province))
        self.assertEqual(PropertyModels.Province.objects.count(), 1)
        self.assertEqual(self.province.name, 'Province 0')

    def test_update_province(self):
        'test update a province'
        self.province.name = 'Province 1'
        self.province.save()
        self.assertEqual(
            PropertyModels.Province.objects.get(id=1).name, 'Province 1'
        )

    def test_unique_province_name_constraint(self):
        'test unique province name constraint'
        with self.assertRaises(Exception) as raised:
            PropertyFactories.ProvinceFactory(name='Province 0')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_province(self):
        'test delete a province'
        self.province.delete()
        self.assertEqual(PropertyModels.Province.objects.count(), 0)
