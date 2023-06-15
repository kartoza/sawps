from django.test import TestCase
from stakeholder.factories import userFactory

from swaps.forms.sign_up import CustomSignupForm

import logging

logger = logging.getLogger(__name__)


class TestCustomSignupForm(TestCase):
    'Test sign up form'

    def setUp(self):
        """
        Sets up before each test
        """

        pass

    def test_user_form(self):
        
        request = {
            'first_name': 'Fan',
            'last_name': 'Andria',
            'email': 'faneva@kartoza.com',
            'password1': 'Test02#FRq8hqcl*@',
            'password2': 'Test02#FRq8hqcl*@',
        }

        form = CustomSignupForm(data=request)
        self.assertEqual(form.is_valid(), True)

        user = userFactory.create()
        user = form.custom_signup(request, user)
        self.assertEqual(user.first_name, request['first_name'])
        self.assertFalse(user.is_active)
