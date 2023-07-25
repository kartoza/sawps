from django.test import (
    TestCase,
    Client,
    RequestFactory
)
from frontend.utils.organisation import CURRENT_ORGANISATION_ID_KEY
from stakeholder.models import (
    Reminders,
    Organisation,
    OrganisationUser
)
from django.urls import reverse
from django.contrib.auth.models import User
from stakeholder.views import NotificationsView
from regulatory_permit.models import DataUsePermission
from stakeholder.models import Reminders
import json
from unittest.mock import patch


class NotificationsViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123454$',
            email='email@gamil.com'
        )
        self.data_use_permission = DataUsePermission.objects.create(
            name="test"
        )
        self.organisation = Organisation.objects.create(
            name="test_organisation",
            data_use_permission = self.data_use_permission
        )
        self.organisation_user = OrganisationUser.objects.create(
            organisation=self.organisation,
            user=self.user
        )
        self.reminder1 = Reminders.objects.create(
            title='Test Reminder 1',
            user=self.user,
            organisation=self.organisation,
            reminder='Test Reminder Note',
            email_sent=True,
            status=Reminders.PASSED
        )
        self.reminder2 = Reminders.objects.create(
            title='Test Reminder 2',
            user=self.user,
            organisation=self.organisation,
            reminder='Test Reminder Note'
        )
        self.client = Client()


    def test_get_notifications(self):

        url = reverse('notifications', kwargs={'slug': self.user.username})
        data = {
            'csrfmiddlewaretoken': self.client.cookies.get('csrftoken', '')
        }
        request = self.factory.get(url, data)
        request.user = self.user
        request.session = {CURRENT_ORGANISATION_ID_KEY: self.organisation}

        # Instantiate the RemindersView and call the get notifications
        view = NotificationsView()
        response = view.get_notifications(request)

        self.assertIsNotNone(response)


    @patch('stakeholder.views.get_reminder_or_notification')
    @patch('stakeholder.views.convert_reminder_dates')
    @patch('frontend.serializers.stakeholder.ReminderSerializer')
    def test_get_notification(
        self,
        mock_reminder,
        mock_convert_dates,
        mock_reminders_serializer):
        url = reverse('notifications', kwargs={'slug': self.user.username})
        data = {
            'action': 'get_notification',
            'ids': [json.dumps(self.reminder1.pk)],
            'csrfmiddlewaretoken': self.client.cookies.get('csrftoken', '')
        }
        request = self.factory.post(url, data)
        request.user = self.user
        request.session = {CURRENT_ORGANISATION_ID_KEY: self.organisation}

        view = NotificationsView()
        response = view.get_notification(request)

        self.assertIsNotNone(response)

    @patch('stakeholder.views.search_reminders_or_notifications')
    @patch('stakeholder.views.convert_reminder_dates')
    @patch('frontend.serializers.stakeholder.ReminderSerializer')
    def test_search_notifications(
        self,
        mock_reminder,
        mock_convert_dates,
        mock_reminders_serializer):
        url = reverse('notifications', kwargs={'slug': self.user.username})
        data = {
            'action': 'search_notifications',
            'query': 'Remin',
            'notifications_page': True,
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        }
        request = self.factory.post(url, data)
        request.user = self.user
        request.session = {CURRENT_ORGANISATION_ID_KEY: self.organisation}

        view = NotificationsView()
        response = view.search_notifications(request)

        self.assertIsNotNone(response)

    @patch('stakeholder.views.delete_reminder_and_notification')
    @patch('stakeholder.views.convert_reminder_dates')
    @patch('frontend.serializers.stakeholder.ReminderSerializer')
    def test_delete_notification(
        self,
        mock_reminder,
        mock_convert_dates,
        mock_reminders_serializer):
        url = reverse('notifications', kwargs={'slug': self.user.username})
        data = {
            'action': 'delete_notification',
            'notifications_page': True,
            'ids': [json.dumps(self.reminder1.pk)],
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        }
        request = self.factory.post(url, data)
        request.user = self.user
        request.session = {CURRENT_ORGANISATION_ID_KEY: self.organisation}

        view = NotificationsView()
        response = view.delete_notification(request)

        self.assertIsNotNone(response)

    def test_dispatch_get_notification(self):
        # Simulate a POST request with action 'get_notification'
        url = reverse('notifications', kwargs={'slug': self.user.username})
        data = {
            'action': 'get_notification',
            'notifications_page': True,
            'ids': [self.reminder1.id],
            'csrfmiddlewaretoken': self.client.cookies.get('csrftoken', ''),
        }
        request = self.factory.post(url, data)
        request.user = self.user
        request.session = {CURRENT_ORGANISATION_ID_KEY: self.organisation}
        view = NotificationsView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_dispatch_search_notifications(self):
        url = reverse('notifications', kwargs={'slug': self.user.username})
        data = {
            'action': 'search_notifications',
            'query': 'i',
            'notifications_page': True,
            'ids': [self.reminder1.id],
            'csrfmiddlewaretoken': self.client.cookies.get('csrftoken', ''),
        }
        request = self.factory.post(url, data)
        request.user = self.user
        request.session = {CURRENT_ORGANISATION_ID_KEY: self.organisation}

        view = NotificationsView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_dispatch_delete_notification(self):
        # Simulate a POST request with action 'delete_notification'
        url = reverse('notifications', kwargs={'slug': self.user.username})
        data = {
            'action': 'delete_notification',
            'notifications_page': True,
            'ids': [self.reminder1.id],
            'csrfmiddlewaretoken': self.client.cookies.get('csrftoken', ''),
        }
        request = self.factory.post(url, data)
        request.user = self.user
        request.session = {CURRENT_ORGANISATION_ID_KEY: self.organisation}

        # Create an instance of the NotificationsView and call the dispatch method
        view = NotificationsView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_dispatch_default_action(self):
        # Simulate a POST request with an invalid action
        url = reverse('notifications', kwargs={'slug': self.user.username})
        data = {
            'action': 'invalid_action',
            'ids': [self.reminder1.id],
            'csrfmiddlewaretoken': self.client.cookies.get('csrftoken', ''),
        }
        request = self.factory.post(url, data)
        request.user = self.user

        view = NotificationsView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 405)

    def test_get_context_data(self):
        # Simulate a GET request to the notifications view
        url = reverse('notifications', kwargs={'slug': self.user.username})
        request = self.factory.get(url)
        request.user = self.user
        request.session = {CURRENT_ORGANISATION_ID_KEY: self.organisation}

        view = NotificationsView.as_view()
        response = view(request)

        self.assertIn('notifications', response.context_data)
