from behave import *
from django.contrib.auth.models import User

use_step_matcher("re")

@given("There is no user")
def step_impl(context):
    pass


@when("I navigate to admin panel")
def step_impl(context):
    super_user = User.objects.create_superuser("admin", "admin@example.com", "admin")
    context.test.client.force_login(super_user)
    context.response = context.test.client.get("/admin/")


@then("status code is (?P<status>\d+)")
def step_impl(context, status):
    code = context.response.status_code
    assert code == int(status), "{0} == {1}".format(code, status)


@then("I create user")
def step_impl(context):
    user = User.objects.create_user("user", "user@example.com", "user")
    #context.test.client.exists(user)
    context.test.client.email = user.email
    context.test.client.name = user.username


@then("user should be present")
def step_impl(context):
    assert context.test.client.email == "user@example.com"
    assert context.test.client.name == "user"
