from django.test import TestCase
from notification.tests.reminder_factory import ReminderF
from notification.models import Reminder


class TestReminder(TestCase):
    """Test for Reminder model"""

    def setUp(self) -> None:
        """setup test data"""
        self.reminder = ReminderF(
            title='title0',
            text= 'text0'
        )

    def test_create_reminder(self):
        """test create reminder"""
        self.assertEqual(self.reminder.title, 'title0')
        self.assertEqual(self.reminder.text, 'text0')
        self.assertEqual(Reminder.objects.count(), 1)

    def test_update_reminder(self):
        """test update reminder"""
        self.reminder.title = 'Test title'
        self.reminder.status = 'draft'
        self.reminder.save()
        self.assertEqual(self.reminder.title, 'Test title')
        self.assertEqual(self.reminder.status, 'draft')

    def test_delete_reminder(self):
        """test delete reminder"""
        self.reminder.delete()
        self.assertEqual(Reminder.objects.count(), 0)
