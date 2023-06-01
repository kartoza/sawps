from django.test import TestCase
from swaps.tests.models.account_factory import (
    UserF,
    GroupF,
)

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

        group = GroupF.create(
            id=1,
            name='Test'
        )
        group.save()

        request = {
            'first_name': 'Fan',
            'last_name': 'Andria',
            'organisation': 'Kartoza',
            'email': 'faneva@kartoza.com',
            'groups': '1',
            'password1': 'Test02',
            'password2': 'Test02'
        }

        user = UserF.create()

        form = CustomSignupForm(data=request)
        self.assertEqual(form.is_valid(), True)

        user = form.custom_signup(request, user)
        self.assertEqual(user.first_name, request['first_name'])
        self.assertEqual(user.organisation, request['organisation'])
        self.assertIsNotNone(user.groups)
