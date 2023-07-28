from frontend.tests.base_view import RegisteredBaseViewTestBase
from frontend.views.home import HomeView


class TestHomeView(RegisteredBaseViewTestBase):
    view_name = 'home'
    view_cls = HomeView

    def test_organisation_selector(self):
        self.do_test_anonymous_user()
        self.do_test_superuser()
        self.do_test_user_with_organisations()
        self.do_test_user_without_organisation()
