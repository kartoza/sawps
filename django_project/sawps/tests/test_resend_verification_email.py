from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail


class ResendVerificationEmailTest(TestCase):

    def test_resend_verification_email(self):
        user = User.objects.create_user(username='testuser',
                                        email='test@example.com',
                                        password='testpassword123',
                                        is_active=False)
        url = reverse('account_resend_verification')
        response = self.client.post(url, {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            'Activate your SAWPS account',
            mail.outbox[0].subject)
