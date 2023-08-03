from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from stakeholder.models import (
    UserProfile
)
from sawps.tests.models.account_factory import UserF
from stakeholder.factories import (
    userProfileFactory,
    userTitleFactory,
    userRoleTypeFactory
)


class TestProfile(TestCase):
    """Tests CURD Profile."""

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
        profile = userProfileFactory.create(
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
        profile = userProfileFactory.create(user=user)
        profile_picture = {
            'picture': 'profile_pictures/picture_P.jpg',
        }
        profile.__dict__.update(profile_picture)
        profile.first_name = 'j'
        profile.last_name = 'jj'
        profile.save()

        user.email = 't@t.com'
        user.save()

        self.assertIsNotNone(profile.picture)
        self.assertIsNotNone(profile.first_name)
        self.assertIsNotNone(profile.last_name)
        self.assertIsNotNone(user.email)

    def test_profile_delete(self):
        """
        Tests profile delete
        """
        user = UserF.create()
        profile = userProfileFactory.create(user=user)
        profile.delete()

        self.assertTrue(profile.pk is None)

    def test_profile_update_request(self):
        """
        Test update profile from the form page
        """
        user = get_user_model().objects.create(
            is_staff=False,
            is_active=True,
            is_superuser=False,
            username='test',
            email='test@test.com',
        )
        title = userTitleFactory.create(
            id=1,
            name = 'test',
        )
        role = userRoleTypeFactory.create(
            id=1,
            name = 'test',
        )
        user.set_password('passwd')
        user.first_name = 'Fan'
        user.last_name = 'Fan'
        user.email = user.email
        user.save()
        UserProfile.objects.create(
            user=user,
            title_id=title,
            user_role_type_id=role
        )
        resp = self.client.login(username='test', password='passwd')
        self.assertTrue(resp)

        post_dict = {
            'first-name': 'Fan',
            'last-name': 'Fan',
            'email': user.email,
            'organization': 'Kartoza',
            'title': '1',
            'role': '1'
        }

        response = self.client.post(
            '/profile/{}/'.format(user.username), post_dict
        )
        self.assertEqual(response.status_code, 302)
        updated_user = get_user_model().objects.get(id=user.id)
        self.assertEqual(updated_user.first_name, post_dict['first-name'])
        self.assertIsNotNone(updated_user.user_profile.picture)
        self.assertEqual(user.user_profile.title_id.name, title.name)
        self.assertEqual(user.user_profile.user_role_type_id.name, role.name)

    def test_context_data(self):
        # Simulate a request with the authenticated user
        user = UserF.create()
        url = reverse('profile', kwargs={'slug': user.username})
        client = Client()
        request = client.get(url)
        request.user = user

        client.force_login(user)
        response = client.get(url, follow=True)

        # Check if the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)
        context = response.context

        self.assertNotIn('titles', context)
        self.assertNotIn('roles', context)
