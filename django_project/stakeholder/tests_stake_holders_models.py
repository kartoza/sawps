from django.test import TestCase
import stakeholder.models as stakholderModels
import stakeholder.factories as stakeholderFactories


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
