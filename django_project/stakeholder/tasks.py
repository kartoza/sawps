from celery import shared_task
from django.utils import timezone
from stakeholder.models import (
    OrganisationUser,
    Reminders,
    UserProfile
)
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.conf import settings


@shared_task
def send_reminder_email(*args):
    reminder = None
    recipient_email = None
    user = None

    if len(args) > 0:
        reminder = args[0]
        try:
            reminder_details = Reminders.objects.get(pk=reminder)
            user = User.objects.get(pk=reminder_details.user.pk)
            recipient_email = user.email
            if len(args) > 1:
                recipient_email = args[1]
        except Exception:
            reminder_details = None

    message = render_to_string(
        'emails/reminder_email.html',
        {
            'domain': Site.objects.get_current().domain,
            'name': user.username,
            'reminder': reminder_details.reminder,
            'date': reminder_details.date,
            'organisation': reminder_details.organisation
        },
    )
    subject = "Reminder: " + reminder_details.title
    send_mail(
        subject,
        None,
        settings.SERVER_EMAIL,
        [recipient_email],
        html_message=message
    )




@shared_task
def send_reminder_emails():
    current_datetime = timezone.now()
    due_reminders = Reminders.objects.filter(
        status=Reminders.ACTIVE,
        email_sent=False,
        date__lte=current_datetime
    )

    for reminder in due_reminders:
        if reminder.type == Reminders.PERSONAL:
            send_reminder_email.delay(reminder.id)
        else:
            org_users_list = OrganisationUser.objects.filter(
                organisation=reminder.organisation
            )
            for org_user in org_users_list:
                send_reminder_email.delay(reminder.id, org_user.user.email)
                try:
                    user_profile = UserProfile.objects.get(user=org_user.user)
                    user_profile.received_notif = False
                    user_profile.save()
                except Exception:
                    continue
        reminder.status = Reminders.PASSED
        reminder.email_sent = True
        reminder.save()
