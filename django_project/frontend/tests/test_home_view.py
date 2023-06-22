from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser
from frontend.tests.model_factories import UserF
from stakeholder.factories import (
    organisationFactory,
    organisationUserFactory
)
from frontend.views.home import HomeView
from django_project.frontend.tests.base_view import RegisteredBaseViewTestBase


class TestHomeView(RegisteredBaseViewTestBase):
    view_name = 'home'
    view_cls = HomeView

    def test_organisation_selector(self):
        self.do_test_anonymous_user()
        self.do_test_superuser()
        self.do_test_user_with_organisations()
        self.do_test_user_without_organisation()
