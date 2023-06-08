from django.test import TestCase
from property.models import PropertyType, Province, ParcelType, Parcel
from property.factories import PropertyTypeFactory, ProvinceFactory, ParcelTypeFactory, ParcelFactory
from django.db.utils import IntegrityError


class PropertyTypeTest(TestCase):
    """propert type test case"""

    @classmethod
    def setUpTestData(cls):
        cls.property_type = PropertyTypeFactory()

    def test_create_property_type(self):
        """test creating a new property type"""
        self.assertTrue(
            isinstance(self.property_type, PropertyType)
        )
        self.assertEqual(PropertyType.objects.count(), 1)
        self.assertEqual(self.property_type.name, 'PropertyType 0')

    def test_update_property_type(self):
        """test updating a property type"""
        self.property_type.name = 'PropertyType 2'
        self.property_type.save()
        self.assertEqual(
            PropertyType.objects.get(id=1).name,
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
        self.assertEqual(PropertyType.objects.count(), 0)


class ProvinceTestCase(TestCase):
    """province test case"""

    @classmethod
    def setUpTestData(cls):
        cls.province = ProvinceFactory()

    def test_create_province(self):
        'test create a province'
        self.assertTrue(isinstance(self.province, Province))
        self.assertEqual(Province.objects.count(), 1)
        self.assertEqual(self.province.name, 'Province 0')

    def test_update_province(self):
        'test update a province'
        self.province.name = 'Province 1'
        self.province.save()
        self.assertEqual(
            Province.objects.get(id=1).name, 'Province 1'
        )

    def test_unique_province_name_constraint(self):
        'test unique province name constraint'
        with self.assertRaises(Exception) as raised:
            ProvinceFactory(name='Province 0')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_province(self):
        'test delete a province'
        self.province.delete()
        self.assertEqual(Province.objects.count(), 0)


class ParcelTypeTestCase(TestCase):
    """Parcel type test case"""
    @classmethod
    def setUpTestData(cls):
        cls.parcel_type = ParcelTypeFactory()
    
    def test_create_parcel_type(self):
        """Test create parcel types """
        self.assertTrue(isinstance(self.parcel_type, ParcelType))
        self.assertEqual(ParcelType.objects.count(), 1)

    def test_update_parcel_type(self):
        """Test update parcel type."""
        self.parcel_type.name = 'ParcelType_1'
        self.parcel_type.save()
        self.assertEqual(ParcelType.objects.all()[0].name, 'ParcelType_1')

    def test_unique_parcel_type_name_constraint(self):
        """Test unique parcel type name constraint."""
        with self.assertRaises(Exception) as raised:
            ParcelTypeFactory(name='ParcelType_1')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_parcel_type(self):
        """Test delete parcel type."""
        self.parcel_type.delete()
        self.assertEqual(ParcelType.objects.count(), 0)


class ParcelTestCase(TestCase):
    """Parcel test case."""
    @classmethod
    def setUpTestData(cls):
        cls.parcel = ParcelFactory()
    
    def test_create_parcel(self):
        """Test create parcel."""
        self.assertTrue(isinstance(self.parcel, Parcel))
        self.assertEqual(Parcel.objects.count(), 1)
        self.assertEqual(self.parcel.sg_number, 'SG_0')
    
    def test_update_parcel(self):
        """Test update parcel."""
        self.parcel.sg_number = 'SG_1'
        self.parcel.save()
        self.assertEqual(Parcel.objects.get(id=1).sg_number, 'SG_1')

    def test_unique_parcel_sg_number_constraint(self):
        """Test unique parcel sg number constraint."""
        with self.assertRaises(Exception) as raised:
            ParcelFactory(sg_number='SG_1')
            self.assertEqual(IntegrityError, type(raised.exception))
    
    def test_delete_parcel(self):
        """Test delete parcel."""
        self.parcel.delete()
        self.assertEqual(Parcel.objects.count(), 0)
