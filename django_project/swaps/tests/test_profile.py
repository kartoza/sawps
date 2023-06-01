from django.contrib.auth import get_user_model
from django.test import TestCase
from swaps.tests.models.account_factory import UserF, ProfileF


class TestProfile(TestCase):
    """ Tests CURD Profile.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_profile_create(self):
        """
        Tests profile creation
        """
        user = UserF.create()
        profile = ProfileF.create(
            user=user,
            picture='profile_pictures/picture_P.jpg',
            )

        self.assertTrue(profile.user is not None)
        self.assertEqual(profile.picture, 'profile_pictures/picture_P.jpg')


    def test_profile_update(self):
        """
        Tests profile update
        """
        user = UserF.create()
        profile = ProfileF.create(
            user=user
        )
        profile_picture = {
            'picture': 'profile_pictures/picture_P.jpg',
        }
        profile.__dict__.update(profile_picture)
        profile.save()

        self.assertIsNotNone(profile.picture)

    def test_profile_delete(self):
        """
        Tests profile delete
        """
        user = UserF.create()
        profile = ProfileF.create(
            user=user
        )
        profile.delete()

        self.assertTrue(profile.pk is None)
