from behave import given, when, then, use_step_matcher
from django.contrib.auth.models import User

use_step_matcher("re")


@given("There is no user")
def no_user(context):
    pass


@when("I navigate to admin panel")
def nav_admin(context):
    super_user = User.objects.create_superuser(
        "admin",
        "admin@example.com",
        "admin"
    )
    context.test.client.force_login(super_user)
    context.response = context.test.client.get("/admin/")


@then("status code is (?P<status>\d+)")
def stat_code(context, status):
    code = context.response.status_code
    assert code == int(status), "{0} == {1}".format(code, status)


@then("I create user")
def create_test_user(context):
    user = User.objects.create_user(
        "user",
        "user@example.com",
        "user"
    )
    # context.test.client.exists(user)
    context.test.client.email = user.email
    context.test.client.name = user.username


@then("user should be present")
def user_is_present(context):
    assert context.test.client.email == "user@example.com"
    assert context.test.client.name == "user"
