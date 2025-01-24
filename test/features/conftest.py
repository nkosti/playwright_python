from playwright.sync_api import expect
from pytest_bdd import given, step, parsers

from test.conftest import Context


@step("Navigate to Home Page")
def navigate_to_home_page(poms: Context):
    poms.landing_pom.open_home_page()


@given(parsers.parse('"{user_role}" navigated to Users page'))
def navigate_to_users_page(poms: Context):
    poms.landing_pom.open_users()


@step(parsers.parse('"{user_role}" navigated to Organizations page'))
def navigate_to_organizations_page(poms: Context):
    poms.landing_pom.open_organizations()


@step("confirmation message is displayed")
def confirmation_message_is_displayed(poms: Context, json_data):
    user = poms.users.create_user
    expect(
        user.page.locator(
            user.locators.SUCCESS_MESSAGE.format(
                json_data.get("Expected").get("expected_message")
            )
        )
    ).to_be_visible()
    poms.users.create_user.close_popup()
