from django.test import (
    TestCase,
    RequestFactory
)
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser
from stakeholder.middleware import UserProfileMiddleware
from frontend.tests.model_factories import UserF
from stakeholder.factories import (
    organisationFactory,
    organisationUserFactory
)
from stakeholder.models import (
    Reminders,
    UserProfile,
    UserRoleType,
    DATA_CONTRIBUTOR_ROLE,
    SUPERUSER_ROLE
)



class RegisteredBaseViewTestBase(TestCase):
    view_name = 'home'
    view_cls = None
    fixtures = ['stakeholder_user_role_types.json']

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware(lambda x: None)
        self.profile_middleware = UserProfileMiddleware(lambda x: None)
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
            user_role_type=UserRoleType.objects.filter(
                name=DATA_CONTRIBUTOR_ROLE
            ).first()
        )
        self.user_profile_1 = UserProfile.objects.create(
            user=self.user_2,
            received_notif=False,
            user_role_type=UserRoleType.objects.filter(
                name=DATA_CONTRIBUTOR_ROLE
            ).first()
        )
        self.user_profile_2 = UserProfile.objects.create(
            user=self.superuser,
            received_notif=False,
            user_role_type=UserRoleType.objects.filter(
                name=SUPERUSER_ROLE
            ).first()
        )

    def process_session(self, request):
        self.middleware.process_request(request)
        self.profile_middleware(request)
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

