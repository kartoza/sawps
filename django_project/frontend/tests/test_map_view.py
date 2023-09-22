from frontend.tests.base_view import RegisteredBaseViewTestBase
from frontend.views.map import MapView
from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponseRedirect


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

    def test_redirect_to_data(self):
        response = self.client.get(reverse('data'))
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response['location'], f"{reverse('map')}?tab=1")

    def test_redirect_to_metrics(self):
        response = self.client.get(reverse('metrics'))
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response['location'], f"{reverse('map')}?tab=2")

    def test_redirect_to_upload(self):
        response = self.client.get(reverse('upload'))
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response['location'], f"{reverse('map')}?tab=3")

    def test_redirect_to_explore(self):
        response = self.client.get(reverse('explore'))
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response['location'], f"{reverse('map')}?tab=0")

