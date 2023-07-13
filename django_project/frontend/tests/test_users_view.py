import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from frontend.views.users import OrganisationUsersView
from regulatory_permit.models import DataUsePermission
from django.core import mail

from stakeholder.models import Organisation, OrganisationInvites, OrganisationUser



class OrganisationUsersViewTest(TestCase):
    """This covers the post, delete_post, and dispatch methods of the view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@gmail.com'
        )
        self.data_use_permission = DataUsePermission.objects.create(
            name="test")
        self.organisation = Organisation.objects.create(
            name="test_organisation", data_use_permission=self.data_use_permission)
        self.organisation_user = OrganisationUser.objects.create(
            organisation=self.organisation, user=self.user)
        self.org_invitation = OrganisationInvites.objects.create(
            email=self.user.email,
            organisation=self.organisation
        )


    def test_delete_post_method(self):
        # url = reverse('Users')
        response = self.client.post(
                '/users/',
                {
                    'action': 'delete',
                    'object_id': self.organisation_user.id,
                    'current_organisation': self.organisation.name
                }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success'})

        # Verify that the OrganisationUser has been deleted
        self.assertFalse(OrganisationUser.objects.filter(
            user=self.organisation_user.user).exists())


    def test_invite_post(self):
        # Create a request object with the required POST data
        response = self.client.post(
            '/users/',
            {
                'action': 'invite',
                'email': 'test@example.com',
                'inviteAs': 'manager',
                'memberRole': 'write',
                'current_organisation': 'test_organisation'
            }
        )

        expected_json = {'status': 'invitation already sent'}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_json)

        # Check email not present
        self.assertEqual(len(mail.outbox), 0)


        
    def test_search_user_table(self):
        # Create a request object with the required POST data
        response = self.client.post(
            '/users/',
            {
                'action': 'search_user_table',
                'query': 'test',
                'current_organisation': 'test_organisation'
            }
        )
                   
        # Assert the expected outcome
        expected_data = [
            {
                'organisation': self.organisation,
                'user': self.user,
                'id': self.user.pk,
                'role': None
            }
        ]
        expected_json = {'data': json.dumps(expected_data)}
            
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_json)
