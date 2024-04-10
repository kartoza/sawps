from frontend.tests.base_view import RegisteredBaseViewTestBase
from frontend.views.logout_view import LogoutView


class TestLogoutView(RegisteredBaseViewTestBase):
    view_name = 'logout'
    view_cls = LogoutView

    def test_organisation_selector(self):
        self.do_test_anonymous_user()
        self.do_test_superuser()
        self.do_test_user_with_organisations()
        self.do_test_user_without_organisation()
        self.do_test_get_current_organisation_with_profile()
        self.do_test_get_or_set_current_organisation_with_superuser()
