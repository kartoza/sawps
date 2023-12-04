import uuid

from django.core import mail
from django.test import (
    Client,
    TestCase,
    RequestFactory
)
from regulatory_permit.models import DataUsePermission
from sawps.tests.models.account_factory import (
    UserF,
    GroupF,
)
from sawps.forms.account_forms import CustomSignupForm
from django.contrib.auth.models import User
from django.urls import reverse
from sawps.views import (
    CustomPasswordResetView,
    AddUserToOrganisation,
    custom_password_reset_complete_view
)
from django.contrib.auth.models import User
from stakeholder.models import (
    Organisation,
    OrganisationInvites,
    OrganisationUser,
    OrganisationRepresentative,
    MEMBER,
    MANAGER
)
from frontend.static_mapping import PROVINCIAL_DATA_CONSUMER, SUPER_USER, ORGANISATION_MEMBER, ORGANISATION_MANAGER

from django_otp.plugins.otp_totp.models import TOTPDevice


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
            password='testpassword',
            first_name='test_user',
            last_name='test_user'
        )

        # Send reset email request
        response = self.client.post(
            reverse('password_reset'),
            {
                    'action': 'sendemail',
                    'email': test_user.email
            }
        )

        self.assertEqual(response.status_code, 200)

        # Check that the email message was sent to the correct user
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn('Password Reset Request', email.subject)
        self.assertIn(test_user.email, email.to)

        test_user.username = None
        response = self.client.post(
            reverse('password_reset'),
            {
                    'action': 'sendemail',
                    'email': test_user.email
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_send_reset_email_invalid_email(self):
        # Simulate a POST request with an invalid email
        url = reverse('password_reset')
        data = {'action': 'sendemail', 'email': 'invalid_email@example.com'}

        # Call the dispatch method
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset.html')
        self.assertEqual(response.context['error_message'], 'The email address is not registered.')

    def test_dispatch_get(self):
        self.factory = RequestFactory()
        url = reverse('password_reset')
        request = self.factory.get(url)

        # Create an instance of the CustomPasswordResetView
        view = CustomPasswordResetView.as_view()

        # Call the dispatch method
        response = view(request)

        # Check that the response is a rendered template
        self.assertEqual(response.status_code, 200)
        self.assertIn('SAWPS', response.content.decode('utf-8'))

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
        self.assertIn('SAWPS', response.content.decode('utf-8'))


class AddUserToOrganisationTestCase(TestCase):
    def setUp(self):
        self.user_email = 'test@example.com'
        self.organisation_name = 'Test Organisation'
        self.user = User.objects.create_user(
            username='testuser',
            email=self.user_email,
            password='testpass',
            first_name='test_user',
            last_name='last_name'
        )
        self.data_use_permission = DataUsePermission.objects.create(
            name="test"
        )
        self.organisation = Organisation.objects.create(
            name=self.organisation_name,
            data_use_permission = self.data_use_permission
        )
        self.organisation2 = Organisation.objects.create(
            name='organisation2',
            data_use_permission = self.data_use_permission
        )
        self.organisation_user = OrganisationUser.objects.create(
            organisation=self.organisation,
            user=self.user
        )
        self.invite = OrganisationInvites.objects.create(
            email=self.user_email,
            organisation=self.organisation
        )
        self.invite_2 = OrganisationInvites.objects.create(
            email=self.user_email,
            organisation=self.organisation2,
            assigned_as=MANAGER
        )

    def test_add_user(self):
        view = AddUserToOrganisation()
        view.adduser(self.invite.uuid)
        org_user = OrganisationUser.objects.filter(
            user=self.user,
            organisation=self.organisation).first()
        org_invite = OrganisationInvites.objects.filter(
            email=self.user_email,
            organisation=self.organisation).first()

        self.assertIsNotNone(org_user)
        self.assertIsNotNone(org_invite)
        self.assertTrue(org_invite.joined)

        # invite_2 is a manager invitation, so Organisation Representative
        # and Organisation User are both created
        view.adduser(self.invite_2.uuid)
        org_user2 = OrganisationUser.objects.filter(
            user=self.user,
            organisation=self.organisation2).first()
        org_rep = OrganisationRepresentative.objects.filter(
            user=self.user,
            organisation=self.organisation2).first()
        self.assertIsNotNone(org_user2)
        self.assertIsNotNone(org_rep)

    def test_is_user_invited(self):
        view = AddUserToOrganisation()
        self.assertTrue(
            view.is_user_invited(
                self.invite.uuid
            )
        )
        self.assertFalse(
            view.is_user_invited(
                uuid.uuid4().hex
            )
        )

    def test_send_invitation_email(self):
        view = AddUserToOrganisation()
        email_details = {
            'return_url': 'http://example.com',
            'user': {'role': 'Admin', 'organisation': 'Test Org'},
            'support_email': 'support@example.com',
            'recipient_email': 'test@example.com',
            'domain': 'example.com',
        }
        success = view.send_invitation_email(email_details)
        self.assertTrue(success)

        fail = view.send_invitation_email([])
        self.assertFalse(fail)


    def test_add_user_view_member(self):
        url = reverse(
            'adduser',
            args=[self.invite.uuid]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        org_user = OrganisationUser.objects.filter(
            user=self.user,
            organisation=self.organisation).first()
        org_invite = OrganisationInvites.objects.filter(
            email=self.user_email,
            organisation=self.organisation).first()
        self.assertIsNotNone(org_user)
        self.assertIsNotNone(org_invite)
        self.assertTrue(org_invite.joined)
        self.assertEquals(org_invite.user, self.user)
        self.assertEquals(org_invite.user.user_profile.current_organisation, self.organisation)
        self.assertTrue(
            ORGANISATION_MEMBER in self.user.groups.values_list('name', flat=True)
        )

    def test_add_user_view_manager(self):
        url = reverse(
            'adduser',
            args=[self.invite_2.uuid]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        org_user = OrganisationRepresentative.objects.filter(
            user=self.user,
            organisation=self.organisation2).first()
        org_invite = OrganisationInvites.objects.filter(
            email=self.user_email,
            organisation=self.organisation2).first()
        self.assertIsNotNone(org_user)
        self.assertIsNotNone(org_invite)
        self.assertTrue(org_invite.joined)
        self.assertEquals(org_invite.user, self.user)
        self.assertEquals(org_invite.user.user_profile.current_organisation, self.organisation2)
        self.assertTrue(
            ORGANISATION_MANAGER in self.user.groups.values_list('name', flat=True)
        )


class SendRequestEmailTestCase(TestCase):
    def test_send_email_success(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='testpass'
        )
        self.client = Client()
        device = TOTPDevice(
            user=user,
            name='device_name'
        )
        device.save()
        resp = self.client.login(
            username='testuser', password='testpass')
        self.assertTrue(resp)
        request = self.client.post(reverse('sendrequest'), data={
            'action': 'sendrequest',
            'organisationName': 'Test Org',
            'message': 'Test message',
        })
        self.assertEqual(request.status_code, 200)
        response_data = request.json()
        self.assertEqual(response_data['status'], 'success')

        request = self.client.post(reverse('sendrequest'))
        self.assertEqual(request.status_code, 405)

        user.last_name = None
        request = self.client.post(reverse('sendrequest'), data={
            'action': 'sendrequest',
            'organisationName': 'Test Org',
            'message': 'Test message',
        })
        self.assertEqual(request.status_code, 200)

