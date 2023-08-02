from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import RequestFactory

class CheckEmailExistsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword'
        )
        self.factory = RequestFactory()

    def test_email_exists(self):
        # Log in the user before making the request
        self.client.force_login(self.user)

        url = reverse('check_email_exists')
        data = {'email': 'test@example.com'}  # Existing email in the database

        # Use self.factory.get() to create a GET request with the user attached
        request = self.factory.get(url, data)
        request.user = self.user

        # Use self.client.get() to create a GET request with the user attached
        response = self.client.get(url, data, HTTP_REFERER='/', follow=True)

        # Check the response status code and content
        self.assertEqual(response.status_code, 200)

    def test_email_not_exists(self):
        # Log in the user before making the request
        self.client.force_login(self.user)

        url = reverse('check_email_exists')
        data = {'email': 'new@example.com'}  # Non-existing email in the database

        # Use self.factory.get() to create a GET request with the user attached
        request = self.factory.get(url, data)
        request.user = self.user

        # Use self.client.get() to create a GET request with the user attached
        response = self.client.get(url, data, HTTP_REFERER='/', follow=True)

        # Check the response status code and content
        self.assertEqual(response.status_code, 200)

    def test_empty_email(self):
        # Log in the user before making the request
        self.client.force_login(self.user)

        url = reverse('check_email_exists')
        data = {'email': ''}

        # Use self.factory.get() to create a GET request with the user attached
        request = self.factory.get(url, data)
        request.user = self.user

        # Use self.client.get() to create a GET request with the user attached
        response = self.client.get(url, data, HTTP_REFERER='/', follow=True)

        # Check the response status code and content
        self.assertEqual(response.status_code, 200)

    def test_same_email_as_current_user(self):
        # Log in the user before making the request
        self.client.force_login(self.user)

        url = reverse('check_email_exists')
        data = {'email': self.user.email}

        # Use self.factory.get() to create a GET request with the user attached
        request = self.factory.get(url, data)
        request.user = self.user

        # Use self.client.get() to create a GET request with the user attached
        response = self.client.get(url, data, HTTP_REFERER='/', follow=True)

        # Check the response status code and content
        self.assertEqual(response.status_code, 200)
