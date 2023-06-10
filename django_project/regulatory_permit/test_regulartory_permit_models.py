from django.test import TestCase
from regulatory_permit.models import DataUsePermission, DataUsePermissionChange
from regulatory_permit.factories import DataUsePermissionFactory, DataUsePermissionChangeFactory
from django.db.utils import IntegrityError
import datetime

class DataUsePermissionTestCase(TestCase):
    """test data use permission model"""

    @classmethod
    def setUpTestData(cls):
        """setup test data"""
        cls.data_use_permission = (
            DataUsePermissionFactory()
        )

    def test_create_data_use_permission(self):
        """test creating use permission"""
        self.assertTrue(
            isinstance(
                self.data_use_permission,
                DataUsePermission,
            )
        )
        self.assertEqual(
            DataUsePermission.objects.count(), 1
        )

    def test_update_data_use_permission(self):
        """test updating use permission"""
        self.data_use_permission.name = 'Data Use Permission #1'
        self.data_use_permission.description = (
            'Data Use Permission Description #1'
        )
        self.data_use_permission.save()
        self.assertEqual(
            DataUsePermission.objects.get(id=self.data_use_permission.id).name,
            'Data Use Permission #1',
        )
        self.assertEqual(
            DataUsePermission.objects.get(
                id=self.data_use_permission.id
            ).description,
            'Data Use Permission Description #1',
        )

    def test_unqiue_data_use_permission_name(self):
        """test unique name of use permission"""
        with self.assertRaises(Exception) as raised:
            DataUsePermission(name='data use permission 0', description='data use permission description 0')
            self.assertEqual(IntegrityError, type(raised.exception))
      
    def test_delete_data_use_permission(self):
        """test deleting use permission"""
        self.data_use_permission.delete()
        self.assertEqual(
            DataUsePermission.objects.count(), 0
        )


class DataUsePermissionChangeTestCase(TestCase):
    """Test case for datausepermission model."""
    @classmethod
    def setUpTestData(cls):
        """setup test data"""
        cls.data_use_permission_change = (
            DataUsePermissionChangeFactory()
        )
    
    def test_create_data_use_permission_change(self):
        """Test create data use permission change."""
        self.assertTrue(
            isinstance(
                self.data_use_permission_change,
                DataUsePermissionChange,
            )
        )
        self.assertEqual(
            DataUsePermissionChange.objects.count(), 1
        )

        self.assertEqual(
            DataUsePermissionChange.objects.get(id=self.data_use_permission_change.id).date.strftime('%Y-%m-%d'),
            self.data_use_permission_change.date,
        )

    def test_update_data_use_permission_change(self):
        """Test update data use permission change."""
        self.data_use_permission_change.date = '2020-01-01'
        self.data_use_permission_change.save()
        date_str = DataUsePermissionChange.objects.get(id=self.data_use_permission_change.id).date.strftime('%Y-%m-%d')
        self.assertEqual(
            date_str,
            '2020-01-01',
        )

    def test_delete_data_use_permission_change(self):
        """Test delete data use permission change."""
        self.data_use_permission_change.delete()
        self.assertEqual(
            DataUsePermissionChange.objects.count(), 0
        )
