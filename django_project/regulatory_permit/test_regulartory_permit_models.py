from django.test import TestCase
import regulatory_permit.models as regulatoryPermitModels
import regulatory_permit.factories as regulatoryPermitFactories
from django.db.utils import IntegrityError


class DataUsePermissionTestCase(TestCase):
    """test data use permission model"""

    @classmethod
    def setUpTestData(cls):
        """setup test data"""
        cls.data_use_permission = (
            regulatoryPermitFactories.DataUsePermissionFactory()
        )

    def test_create_data_use_permission(self):
        """test creating use permission"""
        self.assertTrue(
            isinstance(
                self.data_use_permission,
                regulatoryPermitModels.DataUsePermission,
            )
        )
        self.assertEqual(
            regulatoryPermitModels.DataUsePermission.objects.count(), 1
        )

    def test_update_data_use_permission(self):
        """test updating use permission"""
        self.data_use_permission.name = 'Data Use Permission #1'
        self.data_use_permission.description = (
            'Data Use Permission Description #1'
        )
        self.data_use_permission.save()
        self.assertEqual(
            regulatoryPermitModels.DataUsePermission.objects.get(id=1).name,
            'Data Use Permission #1',
        )
        self.assertEqual(
            regulatoryPermitModels.DataUsePermission.objects.get(
                id=1
            ).description,
            'Data Use Permission Description #1',
        )

    def test_unqiue_data_use_permission_name(self):
        """test unique name of use permission"""
        try:
            (
                regulatoryPermitModels.DataUsePermission.objects.create(
                    name='data use permission 0',
                    description='data use permission description 0',
                )
            )

        except Exception as e:
            self.assertTrue(isinstance(e, IntegrityError))
            return
        self.assertTrue(False)

    def test_delete_data_use_permission(self):
        """test deleting use permission"""
        self.data_use_permission.delete()
        self.assertEqual(
            regulatoryPermitModels.DataUsePermission.objects.count(), 0
        )
