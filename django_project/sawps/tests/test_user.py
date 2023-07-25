from django.core import mail
from django.test import TestCase, RequestFactory
from sawps.tests.models.account_factory import (
    UserF,
    GroupF,
)

from sawps.forms.account_forms import CustomSignupForm
from django.contrib.auth.models import User
from django.urls import reverse
import logging
from sawps.views import (
    CustomPasswordResetView,
    custom_password_reset_complete_view
)

logger = logging.getLogger(__name__)


class TestCustomSignupForm(TestCase):
    'Test sign up form'

    def setUp(self):
        """
        Sets up before each test
        """

        pass

    def test_user_form(self):
        group = GroupF.create(id=1, name='Test')
        group.save()

        request = {
            'first_name': 'Fan',
            'last_name': 'Andria',
            'email': 'faneva@kartoza.com',
            'password1': 'Test02-0000J,sdl',
            'password2': 'Test02-0000J,sdl',
        }

        user = UserF.create()

        form = CustomSignupForm(data=request)
        self.assertEqual(form.is_valid(), True)

        user = form.custom_signup(request, user)
        self.assertEqual(user.first_name, request['first_name'])
        self.assertFalse(user.is_active)


class CustomPasswordResetViewTest(TestCase):
    def test_send_reset_email(self):
        # Create a test user
        test_user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

        # Send reset email request # todo update sendrequest action
        response = self.client.post(
            reverse('password_reset'),
            {
                    'action': 'sendemail',
                    'email': test_user.email
            }
        )

        # Check that the view returns a success response (HTTP 200)
        self.assertEqual(response.status_code, 200)

        # Check that the email message was sent to the correct user
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn('Password Reset Request', email.subject)
        self.assertIn(test_user.email, email.to)

    def test_send_reset_email_invalid_email(self):
        # Simulate a POST request with an invalid email
        self.factory = RequestFactory()
        url = reverse('password_reset')
        data = {'action': 'sendemail', 'email': 'invalid_email@example.com'}
        request = self.factory.post(url, data)

        # Create an instance of the CustomPasswordResetView
        view = CustomPasswordResetView.as_view()

        # Call the dispatch method
        response = view(request)

        self.assertIsNone(response)

    def test_dispatch_get(self):
        # Simulate a GET request to the password reset view
        self.factory = RequestFactory()
        url = reverse('password_reset')
        request = self.factory.get(url)

        # Create an instance of the CustomPasswordResetView
        view = CustomPasswordResetView.as_view()

        # Call the dispatch method
        response = view(request)

        # Check that the response is a rendered template
        self.assertEqual(response.status_code, 200)
        self.assertIn('Password Reset', response.content.decode('utf-8'))

    def test_dispatch_invalid_method(self):
        # Simulate a request with an invalid method
        self.factory = RequestFactory()
        url = reverse('password_reset')
        request = self.factory.put(url)

        # Create an instance of the CustomPasswordResetView
        view = CustomPasswordResetView.as_view()

        # Call the dispatch method
        response = view(request)

        # Check that the response is a 405 Method Not Allowed
        self.assertEqual(response.status_code, 405)


class CustomPasswordResetCompleteViewTest(TestCase):
    def test_custom_password_reset_complete_view(self):
        # Simulate a GET request to the custom password reset complete view
        url = reverse('password_reset_complete')
        request = RequestFactory().get(url)

        # Call the custom_password_reset_complete_view function
        response = custom_password_reset_complete_view(request)

        # Check that the response is a rendered template
        self.assertEqual(response.status_code, 200)
        self.assertIn('Password Reset', response.content.decode('utf-8'))
        self.assertIn('Your Password has been reset successfully .Please proceed to log in',
                      response.content.decode('utf-8'))
