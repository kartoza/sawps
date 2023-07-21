# your_app/tests/test_tasks.py
from django.test import TestCase
from django.utils import timezone
from django.core import mail
from django.contrib.auth.models import User
from stakeholder.tasks import (
    send_reminder_emails,
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
            password='testpassword'
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
        self.reminder = Reminders.objects.create(
            title='test',
            user=self.user,
            organisation=self.organisation,
            reminder='reminder'
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
            # Add other required fields
        )

    def test_send_reminder_emails(self):
        # Call the task to send reminder emails
        send_reminder_emails.apply()

        # Check if the reminder email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, f"Reminder: {self.reminder.title}")
        self.assertIn(self.reminder.reminder, email.body)
        self.assertEqual(email.to, [self.user.email])

        # Check if the reminder status and email_sent fields were updated
        self.reminder.refresh_from_db()
        self.assertEqual(self.reminder.status, Reminders.PASSED)
        self.assertTrue(self.reminder.email_sent)

    def test_send_reminder_email(self):
        # Call the task to send a single reminder email
        send_reminder_email.apply(args=[self.reminder.id])

        # Check if the reminder email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, f"Reminder: {self.reminder.title}")
        self.assertIn(self.reminder.reminder, email.body)
        self.assertEqual(email.to, [self.user.email])
