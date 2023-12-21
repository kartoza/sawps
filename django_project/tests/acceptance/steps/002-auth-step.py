from behave import given, when, then, use_step_matcher
from django.contrib.auth.models import User

use_step_matcher("re")


@given("I am not authenticated")
def not_auth(context):
    pass


@when("I access the page")
def access_page(context):
    context.response = context.test.client.get("/map/")


@then("Status code is (?P<status>\d+)")
def status_code(context, status):
    code = context.response.status_code
    assert code == int(status), "{0} != {1}".format(code, status)


@given("I am authenticated")
def auth_success(context):
    user = User.objects.create_superuser("admin", "admin@example.com", "admin")
    context.test.client.force_login(user)
