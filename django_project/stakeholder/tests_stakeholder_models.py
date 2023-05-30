from django.test import TestCase
import stakeholder.models as stakholderModels
import stakeholder.factories as stakeholderFactories
from django.contrib.auth.models import User


class UserTitleTestCase(TestCase):
    """user title test case, we are"""

    @classmethod
    def setUpTestData(cls):
        cls.userTitle = stakeholderFactories.userTitleFactory()

    def test_create_new_title(self):
        """test creating new title"""
        self.assertEqual(stakholderModels.UserTitle.objects.count(), 1)
        self.assertTrue(self.userTitle.name in ['mr', 'mrs', 'miss', 'dr'])

    def test_update_title(self):
        """test updating a title"""
        self.userTitle.name = 'mr'
        userTitle = stakholderModels.UserTitle.objects.get(
            id=self.userTitle.id
        )
        self.assertTrue(userTitle.name, 'mr')

    def test_delete_new_title(self):
        """test deleting a title"""
        self.userTitle.delete()
        self.assertEqual(stakholderModels.UserTitle.objects.count(), 0)


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
            in ['base user', 'admin', 'super user']
        )

    def test_update_role(self):
        """test updating a role"""
        self.UserRoleTypeFactory.name = 'admin'
        self.UserRoleTypeFactory.save()
        UserRoleObject = stakholderModels.UserRoleType.objects.get(
            id=self.UserRoleTypeFactory.id
        )
        self.assertEqual(UserRoleObject.name, 'admin')

    def test_delete_role(self):
        """test deleting new role"""
        self.UserRoleTypeFactory.delete()
        self.assertEqual(stakholderModels.UserRoleType.objects.count(), 0)


class TestUser(TestCase):
    """test the main user model relation to the profie model"""

    @classmethod
    def setUpTestData(cls):
        cls.profileFactory = stakeholderFactories.userProfileFactory()

    def test_create_new_user_with_new_profile(self):
        """test creating new user when new profile is created"""
        self.assertEqual(stakholderModels.UserProfile.objects.count(), 1)
        self.assertEqual(
            User.objects.count(), 2
        )  # Anon user is created by default

    def test_update_user_profile(self):
        """test updating user through profile"""
        self.profileFactory.user.username = 'test'
        self.profileFactory.user.first_name = 'test123'
        self.profileFactory.user.save()
        self.assertEqual(
            User.objects.get(username='test').first_name, 'test123'
        )

    def test_delete_role(self):
        """test deleting user when a profile is deleted"""
        self.profileFactory.delete()
        self.assertEqual(User.objects.count(), 1)
