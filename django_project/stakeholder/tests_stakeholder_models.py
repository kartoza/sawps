from django.test import TestCase
import stakeholder.models as stakholderModels
import stakeholder.factories as stakeholderFactories


class LoginStatusTestCase(TestCase):
    """user login status test case"""

    @classmethod
    def setUpTestData(cls):
        cls.loginStatus = stakeholderFactories.loginStatusFactory()

    def test_create_login_status(self):
        """test creating login status"""
        self.assertEqual(stakholderModels.LoginStatus.objects.count(), 1)
        self.assertTrue(
            isinstance(self.loginStatus, stakholderModels.LoginStatus)
        )
        self.assertTrue(self.loginStatus.name in ['logged in', 'logged out'])

    def test_update_login_status(self):
        """test updating a login status"""
        self.loginStatus.name = 'logged in'
        loginStatus = stakholderModels.LoginStatus.objects.get(
            id=self.loginStatus.id
        )
        self.assertTrue(loginStatus.name, 'logged in')
        self.loginStatus.name = 'logged out'
        loginStatus = stakholderModels.LoginStatus.objects.get(
            id=self.loginStatus.id
        )
        self.assertTrue(loginStatus.name, 'logged out')

    def test_delete_login_status(self):
        """test deleting a login status"""
        self.loginStatus.delete()
        self.assertEqual(stakholderModels.LoginStatus.objects.count(), 0)
