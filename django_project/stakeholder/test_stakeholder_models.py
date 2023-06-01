from django.test import TestCase
import stakeholder.models as stakholderModels
import stakeholder.factories as stakeholderFactories


class TestUserRoleType(TestCase):
    """test user's role type model"""

    @classmethod
    def setUpTestData(cls):
        cls.UserRoleTypeFactory = stakeholderFactories.userRoleTypeFactory()

    def test_create_new_role(self):
        """test creating new role"""
        self.assertEqual(stakholderModels.UserRoleType.objects.count(), 1)
        self.assertTrue(
            self.UserRoleTypeFactory.name
            in ["base user", "admin", "super user"]
        )

    def test_update_role(self):
        """test updating a role"""
        self.UserRoleTypeFactory.name = "admin"
        self.UserRoleTypeFactory.save()
        UserRoleObject = stakholderModels.UserRoleType.objects.get(
            id=self.UserRoleTypeFactory.id
        )
        self.assertEqual(UserRoleObject.name, "admin")

    def test_delete_role(self):
        """test deleting new role"""
        self.UserRoleTypeFactory.delete()
        self.assertEqual(stakholderModels.UserRoleType.objects.count(), 0)
