import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from frontend.views.organisations import OrganisationsView
from django_otp.plugins.otp_totp.models import TOTPDevice

class OrganisationsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        device = TOTPDevice(
            user=self.user,
            name='device_name'
        )
        device.save()
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('organisations', args=[self.user.username])

    def test_organisations_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organisations.html')
        self.assertIn('organisations', response.context)

    def tearDown(self):
        self.client.logout()

