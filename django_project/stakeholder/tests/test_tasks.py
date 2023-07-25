# your_app/tests/test_tasks.py
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.core import mail
from django.contrib.auth.models import User
from stakeholder.tasks import (
    send_reminder_email
)
from stakeholder.models import (
    OrganisationUser,
    Reminders,
    Organisation
)
from regulatory_permit.models import DataUsePermission


class SendReminderEmailsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@gmail.com'
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

        # Create a test reminder
        self.reminder = Reminders.objects.create(
            user=self.user,
            organisation=self.organisation,
            status=Reminders.ACTIVE,
            email_sent=False,
            title='Test Reminder',
            reminder='Test reminder content',
            date=timezone.now()
        )

    def test_send_reminder_emails(self):
        # Call the task to send reminder emails
        send_reminder_email.apply(args=[self.reminder.id])

        # Check if the reminder email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, f"Reminder: {self.reminder.title}")
        self.assertEqual(email.to, [self.user.email])

    def test_send_reminder_email(self):
        # Call the task to send a single reminder email
        send_reminder_email.apply(args=[self.reminder.id])

        # Check if the reminder email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, f"Reminder: {self.reminder.title}")
        self.assertEqual(email.to, [self.user.email])
