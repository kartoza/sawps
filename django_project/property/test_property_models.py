from django.test import TestCase
from property.models import PropertyType, Province, OwnershipStatus
from property.factories import PropertyTypeFactory, ProvinceFactory, OwnershipStatusFactory
from django.db.utils import IntegrityError


class PropertyTypeTest(TestCase):
    """Propert type test case"""

    @classmethod
    def setUpTestData(cls):
        cls.property_type = PropertyTypeFactory()

    def test_create_property_type(self):
        """Test creating a new property type"""
        self.assertTrue(
            isinstance(self.property_type, PropertyType)
        )
        self.assertEqual(PropertyType.objects.count(), 1)
        self.assertEqual(self.property_type.name, 'PropertyType 0')

    def test_update_property_type(self):
        """Test updating a property type"""
        self.property_type.name = 'PropertyType 2'
        self.property_type.save()
        self.assertEqual(
            PropertyType.objects.get(id=1).name,
            'PropertyType 2',
        )

    def test_property_type_unique_name_constraint(self):
        """Test property type unique name constraint"""
        with self.assertRaises(Exception) as raised:
            PropertyTypeFactory(name='PropertyType 2')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_property_type(self):
        """Test deleting a property type"""
        self.property_type.delete()
        self.assertEqual(PropertyType.objects.count(), 0)


class ProvinceTestCase(TestCase):
    """Province test case"""

    @classmethod
    def setUpTestData(cls):
        cls.province = ProvinceFactory()

    def test_create_province(self):
        'Test create a province.'
        self.assertTrue(isinstance(self.province, Province))
        self.assertEqual(Province.objects.count(), 1)
        self.assertEqual(self.province.name, 'Province 0')

    def test_update_province(self):
        'Test update a province.'
        self.province.name = 'Province 1'
        self.province.save()
        self.assertEqual(
            Province.objects.get(id=1).name, 'Province 1'
        )

    def test_unique_province_name_constraint(self):
        'Test unique province name constraint.'
        with self.assertRaises(Exception) as raised:
            ProvinceFactory(name='Province 0')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_province(self):
        'Test delete a province.'
        self.province.delete()
        self.assertEqual(Province.objects.count(), 0)


class OwnershipStatusTestCase(TestCase):
    """ Ownership Status test case."""
    @classmethod
    def setUpTestData(cls):
        cls.ownership_status = OwnershipStatusFactory()

    def test_create_ownership_status(self):
        """ test creating ownership status """
        self.assertTrue(isinstance(self.ownership_status, OwnershipStatus))
        self.assertEqual(OwnershipStatus.objects.count(), 1)
        self.assertEqual(self.ownership_status.name, 'OwnershipStatus_0')

    def test_update_ownership_status(self):
        """Test update ownership status."""
        self.ownership_status.name = 'OwnershipStatus_1'
        self.ownership_status.save()
        self.assertEqual(OwnershipStatus.objects.get(id=1).name, 'OwnershipStatus_1')

    def test_ownership_status_unique_name_constraint(self):
        """Test ownership status unique name constraint."""
        with self.assertRaises(Exception) as raised:
            OwnershipStatusFactory(name='OwnershipStatus_1')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_ownership_status(self):
        """Test delete ownership status."""
        self.ownership_status.delete()
        self.assertEqual(OwnershipStatus.objects.count(), 0)
