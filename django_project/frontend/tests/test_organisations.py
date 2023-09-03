import json
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from regulatory_permit.models import DataUsePermission
from stakeholder.factories import userProfileFactory
from frontend.views.organisations import OrganisationsView
from frontend.views.switch_organisation import switch_organisation
from django_otp.plugins.otp_totp.models import TOTPDevice
from stakeholder.models import OrganisationUser, Organisation

class OrganisationsViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.data_use_permission = DataUsePermission.objects.create(
            name="test"
        )
        self.organisation = Organisation.objects.create(
            name="test_organisation",
            data_use_permission=self.data_use_permission
        )
        userProfileFactory.create(
            user=self.user
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


    def test_switch_organisation_with_none_organisation_user(self):
        # Login as the regular user
        self.client.login(username='testuser', password='testpassword')

        # Switch to the organisation
        response = self.client.get(
            reverse(
                'switch-organisation',
                args=[self.organisation.id]
                )
            )

        # Assert that the response is a redirect to the homepage
        self.assertEqual(response.status_code, 403)

    def test_switch_organisation_with_organisation_user(self):
        OrganisationUser.objects.create(
            organisation=self.organisation,
            user=self.user
        )
        # Login as the regular user
        self.client.login(username='testuser', password='testpassword')

        # Attempt to switch to the organisation
        response = self.client.get(
            reverse(
                'switch-organisation',
                args=[self.organisation.id]
                )
            )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def tearDown(self):
        self.client.logout()

