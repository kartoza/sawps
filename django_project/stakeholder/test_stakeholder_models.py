from django.test import TestCase
from stakeholder.models import UserRoleType, UserTitle, LoginStatus, UserProfile
from stakeholder.factories import userRoleTypeFactory, userTitleFactory, loginStatusFactory, userFactory, userProfileFactory
from django.contrib.auth.models import User


class TestUserRoleType(TestCase):
    """test user's role type model"""

    @classmethod
    def setUpTestData(cls):
        cls.UserRoleTypeFactory = userRoleTypeFactory()

    def test_create_new_role(self):
        """test creating new role"""
        self.assertEqual(UserRoleType.objects.count(), 1)
        self.assertTrue(
            self.UserRoleTypeFactory.name
            in ['base user', 'admin', 'super user']
        )

    def test_update_role(self):
        """test updating a role"""
        self.UserRoleTypeFactory.name = 'admin'
        self.UserRoleTypeFactory.save()
        UserRoleObject = UserRoleType.objects.get(
            id=self.UserRoleTypeFactory.id
        )
        self.assertEqual(UserRoleObject.name, 'admin')

    def test_delete_role(self):
        """test deleting new role"""
        self.UserRoleTypeFactory.delete()
        self.assertEqual(UserRoleType.objects.count(), 0)


class UserTitleTestCase(TestCase):
    """user title test case, we are"""

    @classmethod
    def setUpTestData(cls):
        cls.userTitle = userTitleFactory()

    def test_create_new_title(self):
        """test creating new title"""
        self.assertEqual(UserTitle.objects.count(), 1)
        self.assertTrue(self.userTitle.name in ['mr', 'mrs', 'miss', 'dr'])

    def test_update_title(self):
        """test updating a title"""
        self.userTitle.name = 'mr'
        userTitle = UserTitle.objects.get(id=self.userTitle.id)
        self.assertTrue(userTitle.name, 'mr')

    def test_delete_new_title(self):
        """test deleting a title"""
        self.userTitle.delete()
        self.assertEqual(UserTitle.objects.count(), 0)


class LoginStatusTestCase(TestCase):
    """user login status test case"""

    @classmethod
    def setUpTestData(cls):
        cls.loginStatus = loginStatusFactory()

    def test_create_login_status(self):
        """test creating login status"""
        self.assertEqual(LoginStatus.objects.count(), 1)
        self.assertTrue(
            isinstance(self.loginStatus, LoginStatus)
        )
        self.assertTrue(self.loginStatus.name in ['logged in', 'logged out'])

    def test_update_login_status(self):
        """test updating a login status"""
        self.loginStatus.name = 'logged in'
        loginStatus = LoginStatus.objects.get(
            id=self.loginStatus.id
        )
        self.assertTrue(loginStatus.name, 'logged in')
        self.loginStatus.name = 'logged out'
        loginStatus = LoginStatus.objects.get(
            id=self.loginStatus.id
        )
        self.assertTrue(loginStatus.name, 'logged out')

    def test_delete_login_status(self):
        """test deleting a login status"""
        self.loginStatus.delete()
        self.assertEqual(LoginStatus.objects.count(), 0)


class TestUser(TestCase):
    """test the main user model relation to the profie model"""

    @classmethod
    def setUpTestData(cls):
        cls.profileFactory = userProfileFactory()

    def test_create_new_user_with_new_profile(self):
        """test creating new user when new profile is created"""
        self.assertEqual(UserProfile.objects.count(), 1)
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