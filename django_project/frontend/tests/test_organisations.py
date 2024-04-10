from django.core import mail
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from regulatory_permit.models import DataUsePermission
from django_otp.plugins.otp_totp.models import TOTPDevice
from stakeholder.models import OrganisationUser, Organisation
from stakeholder.factories import (
    organisationFactory,
)
from stakeholder.views import OrganisationAPIView
from property.factories import (
    ProvinceFactory
)
from frontend.tests.model_factories import UserF
from property.factories import PropertyFactory
from frontend.tests.request_factories import OrganisationAPIRequestFactory
from rest_framework import status
from stakeholder.factories import organisationUserFactory
from frontend.static_mapping import (
    PROVINCIAL_DATA_SCIENTIST,
    NATIONAL_DATA_CONSUMER,
    ORGANISATION_MEMBER,
    ORGANISATION_MANAGER
)


class OrganisationsViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.organisation = Organisation.objects.create(
            name="test_organisation"
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


class TestOrganisationAPIView(TestCase):
    def setUp(self) -> None:
        self.province = ProvinceFactory.create()

        #create organisation
        self.organisation_1 = organisationFactory.create(
            national=False,
            province=self.province
        )
        self.organisation_2 = organisationFactory.create(national=True)

        # create user
        self.user_1 = UserF.create(username='test_1')
        self.user_2 = UserF.create(username='test_2')
        # create group organisation member and manager
        self.group_member, _ = Group.objects.get_or_create(name=ORGANISATION_MEMBER)
        self.group_manager, _ = Group.objects.get_or_create(name=ORGANISATION_MANAGER)

    def test_organisation_list(self):
        """Test organisation for organisation member"""
        factory = OrganisationAPIRequestFactory(self.organisation_1)
        organisationUserFactory.create(
            organisation=self.organisation_1,
            user=self.user_1
        )
        request = factory.get(
            reverse('organisation')
        )
        request.user = self.user_1
        view = OrganisationAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        # assert can see his own organisation
        self.assertEqual(len(response.data), 1)
        _organisation = response.data[0]
        self.assertEqual(_organisation['id'], self.organisation_1.id)
        self.assertEqual(_organisation['name'], self.organisation_1.name)

    def test_organisation_list_for_national(self):
        """Test organisation for national roles"""
        national_dc_group, _ = Group.objects.get_or_create(name=NATIONAL_DATA_CONSUMER)
        factory = OrganisationAPIRequestFactory(self.organisation_2)
        organisationUserFactory.create(
            organisation=self.organisation_2,
            user=self.user_1
        )
        self.user_1.groups.add(national_dc_group)

        request = factory.get(
            reverse('organisation')
        )
        request.user = self.user_1
        view = OrganisationAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        # assert can see all organisations
        self.assertEqual(len(response.data), 2)

    def test_organisation_list_for_provincial(self):
        """Test organisation for provincial roles"""
        provincial_ds_group, _ = Group.objects.get_or_create(name=PROVINCIAL_DATA_SCIENTIST)
        PropertyFactory.create(
            province=self.province,
            organisation=self.organisation_1
        )
        self.user_1.user_profile.current_organisation = self.organisation_1
        self.user_1.save()
        self.user_1.groups.add(provincial_ds_group)
        self.organisation_1.province = None
        self.organisation_1.save()
        factory = OrganisationAPIRequestFactory(self.organisation_1)
        # test with empty province
        request = factory.get(
            reverse('organisation')
        )
        request.user = self.user_1
        view = OrganisationAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        # test with empty current organisation
        self.organisation_1.province = self.province
        self.organisation_1.save()
        self.user_1.user_profile.current_organisation = None
        self.user_1.save()
        request = factory.get(
            reverse('organisation')
        )
        request.user = self.user_1
        view = OrganisationAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        # test with existing province
        self.user_1.user_profile.current_organisation = self.organisation_1
        self.user_1.save()
        request = factory.get(
            reverse('organisation')
        )
        request.user = self.user_1
        view = OrganisationAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        find_organisation = [org for org in response.data if org['id'] == self.organisation_1.id]
        self.assertEqual(len(find_organisation), 1)
        # assert can see diff organisation in same province
        property_2 = PropertyFactory.create(
            province=self.province,
            organisation=self.organisation_2
        )
        request = factory.get(
            reverse('organisation')
        )
        request.user = self.user_1
        view = OrganisationAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        find_organisation = [org for org in response.data if org['id'] == self.organisation_1.id]
        self.assertEqual(len(find_organisation), 1)
        find_organisation = [org for org in response.data if org['id'] == self.organisation_2.id]
        self.assertEqual(len(find_organisation), 1)
        # assert cannot see organisation in other province
        property_2.province = ProvinceFactory.create()
        property_2.save()
        request = factory.get(
            reverse('organisation')
        )
        request.user = self.user_1
        view = OrganisationAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        find_organisation = [org for org in response.data if org['id'] == self.organisation_1.id]
        self.assertEqual(len(find_organisation), 1)


class OrganisationTests(TestCase):

    def setUp(self):
        self.organisation = organisationFactory.create(
            name="Test Organisation",
            hosting_through_sanbi_platforms=True
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.superuser = User.objects.create_user(
            username='superuser',
            password='testpassword',
            is_superuser=True,
            email='super@user.com'
        )
        device = TOTPDevice(
            user=self.user,
            name='device_name'
        )
        device.save()
        self.client.login(username='testuser', password='testpassword')

    def test_save_permissions_valid_request(self):
        data = {
            'only_sanbi': 'true',
            'hosting_data_sanbi': 'false',
            'hosting_data_sanbi_other': 'true',
        }
        url = reverse('save_permissions', args=[self.organisation.id])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.organisation.refresh_from_db()
        self.assertTrue(self.organisation.use_of_data_by_sanbi_only)
        self.assertFalse(self.organisation.hosting_through_sanbi_platforms)
        self.assertTrue(self.organisation.allowing_sanbi_to_expose_data)
        self.assertIn(
            f'Changes to {self.organisation.name}\'s Permissions Settings',
            mail.outbox[0].subject)

    def test_save_permissions_invalid_request(self):
        data = {}  # Invalid request with missing data
        url = reverse('save_permissions', args=[self.organisation.id])
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_save_permissions_organisation_not_found(self):
        data = {
            'only_sanbi': 'true',
            'hosting_data_sanbi': 'false',
            'hosting_data_sanbi_other': 'true',
        }
        invalid_org_id = self.organisation.id + 1  # Non-existent ID
        url = reverse('save_permissions', args=[invalid_org_id])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_organization_detail_valid(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('organization_detail_by_id', args=[self.organisation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test Organisation')

    def test_organization_detail_invalid(self):
        self.client.login(username='testuser', password='testpassword')
        invalid_org_id = self.organisation.id + 1  # Non-existent ID
        url = reverse('organization_detail_by_id', args=[invalid_org_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

