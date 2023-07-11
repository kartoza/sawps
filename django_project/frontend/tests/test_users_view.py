from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from regulatory_permit.models import DataUsePermission
from django.core import mail

from stakeholder.models import Organisation, OrganisationUser



class OrganisationUsersViewTest(TestCase):
    """This covers the post, delete_post, and dispatch methods of the view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.data_use_permission = DataUsePermission.objects.create(
            name="test")
        self.organisation = Organisation.objects.create(
            name="test_organisation", data_use_permission=self.data_use_permission)
        self.organisation_user = OrganisationUser.objects.create(
            organisation=self.organisation, user=self.user)


    def test_delete_post_method(self):
        data = {'action': 'delete', 'object_id': self.organisation_user.id}
        url = reverse('Users')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success'})
        OrganisationUser.objects.filter(
            user=self.organisation_user.user).delete()

        self.assertEqual(OrganisationUser.objects.filter(
            user=self.organisation_user.user).exists(), False)

    def test_invite_post(self):
        url = reverse('Users')
        data = {
            'action': 'invite',
            'email': 'test@example.com',
            'inviteAs': 'manager',
            'memberRole': 'write',
            'current_organisation': 'Test Organisation',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'success')

        # Check email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'ORGANISATION INVITATION')
