from frontend.tests.base_view import RegisteredBaseViewTestBase
from frontend.views.map import MapView
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from sawps.tests.models.account_factory import GroupF, UserF
from sawps.models import ExtendedGroup
from frontend.static_mapping import (
    NATIONAL_DATA_CONSUMER,
    NATIONAL_DATA_SCIENTIST,
    ORGANISATION_MEMBER
)


class TestHomeView(RegisteredBaseViewTestBase):
    view_name = 'map'
    view_cls = MapView

    def test_organisation_selector(self):
        self.do_test_anonymous_user()
        self.do_test_superuser()
        self.do_test_user_with_organisations()
        self.do_test_user_without_organisation()


class RedirectViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        # create new super user
        self.user_1 = UserF.create(is_superuser=True)
        # create another user for data consumer
        self.user_2 = UserF.create(username='test_2')
        self.data_consumer_group = GroupF.create(name=NATIONAL_DATA_CONSUMER)
        self.user_2.groups.add(self.data_consumer_group)
        # create organisation member group with all permission
        group_1, _ = Group.objects.get_or_create(name=ORGANISATION_MEMBER)
        content_type = ContentType.objects.get_for_model(ExtendedGroup)
        all_permissions = Permission.objects.filter(content_type=content_type)
        for perm in all_permissions:
            group_1.permissions.add(perm)
        self.user_2.groups.add(group_1)
        # create data scientist group
        self.data_scientist_group = GroupF.create(name=NATIONAL_DATA_SCIENTIST)
        self.user_3 = UserF.create(username='test_3')
        self.user_3.groups.add(self.data_scientist_group)
        self.user_3.groups.add(group_1)

    def test_redirect_to_report(self):
        response = self.client.get(reverse('reports'))
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response['location'], f"{reverse('map')}?tab=1")

    def test_redirect_to_charts(self):
        response = self.client.get(reverse('charts'))
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response['location'], f"{reverse('map')}?tab=2")

    def test_redirect_to_trends(self):
        response = self.client.get(reverse('trends'))
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response['location'], f"{reverse('map')}?tab=3")

    def test_redirect_to_upload(self):
        response = self.client.get(reverse('upload'))
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response['location'], f"{reverse('map')}?tab=4")

    def test_redirect_to_explore(self):
        response = self.client.get(reverse('explore'))
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response['location'], f"{reverse('map')}?tab=0")

    def test_data_consumer_access_upload(self):
        request = self.factory.get(f"{reverse('map')}?tab=4")
        request.user = self.user_2
        view = MapView()
        view.setup(request)
        with self.assertRaises(PermissionDenied):
            view.get_context_data()

    def test_data_scientist_access_upload(self):
        request = self.factory.get(f"{reverse('map')}?tab=4")
        request.user = self.user_3
        view = MapView()
        view.setup(request)
        ctx = view.get_context_data()
        self.assertIn('can_user_do_upload_data', ctx)
        self.assertTrue(ctx['can_user_do_upload_data'])

    def test_superuser_data_upload_access(self):
        request = self.factory.get(f"{reverse('map')}?tab=4")
        request.user = self.user_1
        view = MapView()
        view.setup(request)
        ctx = view.get_context_data()
        self.assertIn('can_user_do_upload_data', ctx)
        self.assertTrue(ctx['can_user_do_upload_data'])
