from django.test import TestCase
import regulatory_permit.models as regulatoryPermitModels
import regulatory_permit.factories as regulatoryPermitFactories


class DataUsePermissionTest(TestCase):
    """ data user permission model test case """
    @classmethod
    def setUpTestData(cls) -> None:
        """ setup data for permission model test case """
        cls.usePermission = regulatoryPermitFactories.dataUsePermissionFactory()

    def test_create_data_use_permission(self):
        """ test creating data use permission """
        self.assertEqual(regulatoryPermitModels.dataUsePermission.objects.count(), 1)
        self.assertEqual(self.usePermission.name,"Data use permission")

    def test_update_data_use_permission(self):
        """ test updating data use permission """
        usePermission = regulatoryPermitModels.dataUsePermission.objects.get(id=1)
        usePermission.name = "Data use permission updated"
        usePermission.save()
        self.assertEqual(regulatoryPermitModels.dataUsePermission.objects.get(id=1).name, "Data use permission updated")

    def test_delete_data_use_permission(self):
        """ test deleting data use permission """
        self.usePermission.delete()
        self.assertEqual(regulatoryPermitModels.dataUsePermission.objects.count(), 0)
