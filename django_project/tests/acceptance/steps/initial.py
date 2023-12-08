from behave import given, when, then, use_step_matcher
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# uses regex to match
use_step_matcher("re")

# global variables
chrome_options = Options()
#chrome_options.add_argument("--headless")


@given("the user is on the landingpage")
def step_user_is_on_homepage(context):
    context.selenium = webdriver.chrome(options=chrome_options)
    # homepage
    context.selenium.get(f"http://127.0.0.1:61100/")


@then("page is landingpage")
def step_page_is_homepage(context):
    # Assert that the title matches the expected title
    expected_title = "SAWPS"
    assert context.selenium.title == expected_title
    # Close the browser window
    context.selenium.quit()


@given("user is on 'landingpage'")
def step_user_is_on_landingpage(context):
    context.selenium = webdriver.chrome(options=chrome_options)
    # login to admin panel
    # homepage
    context.selenium.get(f"http://127.0.0.1:61100/")
    context.selenium.find_element(By.LINK_TEXT, 'Admin Page').click()


@when("user clicks on 'Log in'")
def step_clicks_on_login(context):
    # fill in login information
    username = context.selenium.find_element(By.ID, 'id_login')
    username.send_keys("admin@example.com")
    password = context.selenium.find_element(By.ID, 'id_password')
    password.send_keys("admin")

    # locate login button and click on it
    context.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()


@then("page is 'landingpage with explore and upload data button visible'")
def step_page_is_on_landingpage(context):
    # Assert that the title matches the expected title
    expected_title = "Landing page"
    assert context.selenium.title == expected_title
    # Close the browser window
    context.selenium.quit()


@given("user is on the landingpage")
def step_user_is_on_homepage(context):
    context.selenium = webdriver.chrome(options=chrome_options)
    # homepage
    context.selenium.get(f"http://127.0.0.1:61100/")


@when("user clicks on 'Explore' link")
def step_clicks_on_poi(context):
    context.selenium.find_element(By.LINK_TEXT, 'Explore').click()


@then("the page is the'map' page")
def step_page_is_poi(context):
    # Assert that the title matches the expected title
    expected_title = "map"
    assert context.selenium.title == expected_title
    # Close the browser window
    context.selenium.quit()