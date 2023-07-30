from django.test import (
    TestCase,
    RequestFactory
)
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser
from frontend.utils.organisation import CURRENT_ORGANISATION_ID_KEY
from frontend.views.base_view import get_user_notifications
from frontend.tests.model_factories import UserF
from stakeholder.factories import (
    organisationFactory,
    organisationUserFactory
)
from stakeholder.models import (
    Reminders,
    UserProfile
)
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import datetime
from django.contrib.messages.storage.fallback import FallbackStorage



class RegisteredBaseViewTestBase(TestCase):
    view_name = 'home'
    view_cls = None

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware(lambda x: None)
        self.user_1 = UserF.create(username='test_1')
        self.superuser = UserF.create(
            username='test_2',
            is_superuser=True
        )
        self.user_2 = UserF.create(username='test_3')
        self.organisation_1 = organisationFactory.create()
        self.organisation_2 = organisationFactory.create()
        self.organisation_3 = organisationFactory.create()
        # add user 1 to organisation 1 and 3
        organisationUserFactory.create(
            user=self.user_1,
            organisation=self.organisation_1
        )
        organisationUserFactory.create(
            user=self.user_1,
            organisation=self.organisation_3
        )
        self.reminder = Reminders.objects.create(
            user=self.user_1,
            organisation=self.organisation_1,
            status=Reminders.PASSED,
            email_sent=True,
            title='Test Reminder 1',
            reminder='Test Reminder'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user_1,
            received_notif=False
        )

    def process_session(self, request):
        self.middleware.process_request(request)
        request.session.save()

    def do_test_anonymous_user(self):
        request = self.factory.get(reverse(self.view_name))
        request.user = AnonymousUser()
        self.process_session(request)
        view = self.view_cls()
        view.setup(request)
        context = view.get_context_data()
        self.assertNotIn('organisations', context)
        self.assertNotIn('current_organisation_id', context)

    def do_test_superuser(self):
        request = self.factory.get(reverse(self.view_name))
        request.user = self.superuser
        self.process_session(request)
        view = self.view_cls()
        view.setup(request)
        context = view.get_context_data()
        self.assertIn('organisations', context)
        self.assertEqual(len(context['organisations']), 2)
        self.assertIn('current_organisation_id', context)
        self.assertNotIn(context['current_organisation_id'],
                         [org['id'] for org in context['organisations']])

    def do_test_user_with_organisations(self):
        request = self.factory.get(reverse(self.view_name))
        request.user = self.user_1
        self.process_session(request)
        view = self.view_cls()
        view.setup(request)
        context = view.get_context_data()
        self.assertIn('current_organisation_id', context)
        self.assertIn('organisations', context)
        self.assertEqual(len(context['organisations']), 1)
        self.assertNotEqual(context['organisations'][0]['id'],
                            context['current_organisation_id'])

    def do_test_user_without_organisation(self):
        request = self.factory.get(reverse(self.view_name))
        request.user = self.user_2
        self.process_session(request)
        view = self.view_cls()
        view.setup(request)
        context = view.get_context_data()
        self.assertIn('organisations', context)
        self.assertEqual(len(context['organisations']), 0)
        self.assertIn('current_organisation_id', context)
        self.assertEqual(context['current_organisation_id'], 0)


class GetUserNotificationsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        # Create a test user profile
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            received_notif=False
        )
        # create organisation
        self.organisation = organisationFactory.create()
        # Create a test reminder
        self.reminder = Reminders.objects.create(
            user=self.user,
            organisation=self.organisation,
            status=Reminders.PASSED,
            email_sent=True,
            date=datetime.now()
        )

    def test_get_user_notifications(self):
        # Simulate a request to the view
        request = RequestFactory().get('get_user_notifications')
        request.user = self.user
        request.session = {CURRENT_ORGANISATION_ID_KEY: self.organisation.pk} 

        # Add a message storage to the request
        setattr(request, '_messages', FallbackStorage(request))

        # Call the view function
        response = get_user_notifications(request)

        # Check that the view returns a JsonResponse
        self.assertIsInstance(response, JsonResponse)

        # Check that the status in the JsonResponse is 'success'
        self.assertEqual(response.json()['status'], 'success')

        # Check that the 'user_notifications' key in the JsonResponse contains the reminder title
        self.assertEqual(response.json()['user_notifications'], [self.reminder.title])

        # Check that the UserProfile received_notif is set to True
        self.assertTrue(UserProfile.objects.get(user=self.user).received_notif)

        # test messages were added
        messages = list(get_messages(response))
        self.assertTrue(len(messages) == 1)

