from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status
from django.test import TestCase, override_settings
from notification.tests.reminder_factory import ReminderF
from sawps.tests.models.account_factory import UserF


class TestApiView(TestCase):
    """Test all api view"""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = UserF.create(is_superuser=True)

    @override_settings(DISABLE_2FA=True)
    def test_get_reminder_api(self):
        """Test reminder api"""
        ReminderF.create(
            id=1,
            title='Title test 1',
            text='Reminder text 1',
            status='active',
        )

        self.client.login(username=self.user.username, password='password')

        pk = '1'
        api_url = '/api/reminder/?reminderId=' + pk
        response = self.client.get(api_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)

    @override_settings(DISABLE_2FA=True)
    def test_list_reminders_api(self):
        """Test reminder aip"""
        ReminderF.create(
            id=1,
            title='Title test 1',
            text='Reminder text 1',
            status='active',
        )
        ReminderF.create(
            title='Title test 2',
            text='Reminder text 2',
            status='active',
        )

        self.client.login(username=self.user.username, password='password')

        reminder_status = 'active'
        api_url = '/api/reminders/?status=' + reminder_status
        response = self.client.get(api_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
