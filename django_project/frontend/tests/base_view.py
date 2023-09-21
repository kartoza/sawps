from django.test import (
    TestCase,
    RequestFactory
)
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from frontend.views.base_view import RegisteredOrganisationBaseView
from django.contrib.auth.models import AnonymousUser
from frontend.tests.model_factories import UserF
from stakeholder.factories import (
    organisationFactory,
    organisationUserFactory
)
from stakeholder.models import (
    Reminders,
    UserProfile
)



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
            received_notif=False,
            current_organisation=self.organisation_1
        )
        self.superuser.user_profile = UserProfile.objects.create(
            user=self.superuser,
            current_organisation=self.organisation_1
        )
        self.user_2.user_profile = UserProfile.objects.create(
            user=self.user_2
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
        self.assertEqual(len(context['organisations']), 2)
        self.assertNotEqual(context['organisations'][1]['id'],
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

    def do_test_get_current_organisation_with_profile(self):

        # Create a request
        request = self.factory.get(reverse(self.view_name))

        # Attach the user to the request
        request.user = self.user_1

        # Create an instance of the view and call the method
        view = RegisteredOrganisationBaseView()
        view.request = request

        # Test that the method returns the correct current organisation
        current_organisation = view.get_current_organisation()
        self.assertIsNotNone(current_organisation)

    def do_test_get_or_set_current_organisation_with_superuser(self):

        # Create a request
        request = self.factory.get(reverse(self.view_name))

        # Attach the user to the request
        request.user = self.superuser

        # Create an instance of the view and call the method
        view = RegisteredOrganisationBaseView()
        view.request = request

        # Test that the method returns the correct current organisation
        current_organisation = view.get_or_set_current_organisation()
        self.assertIsNotNone(current_organisation)

