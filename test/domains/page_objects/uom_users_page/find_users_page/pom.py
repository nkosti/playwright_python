import logging
from typing import Literal

from playwright.sync_api import Page, TimeoutError

from test.domains.enum.users.users import UserFiltersCell
from test.domains.page_objects.base_pom.base_pom import BasePOM
from .locators import Locators


class FindUserPOM(BasePOM):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = Locators
        self.page = page

    def create_new_user(self, email: str):
        self.click_element(self.locators.CREATE_BUTTON)
        self.type_in_element(self.locators.NEW_USER_EMAIL_INPUT, email)
        self.click_element(self.locators.ADD_USER_BUTTON)

    def search_user_by(
            self,
            username: str = None,
            first_name: str = None,
            last_name: str = None,
            email: str = None,
            org_name: str = None,
    ):
        """
        How to use:
        Example 1: Search by username and email
        `search_user_by(username="john_doe", email="john.doe@example.com")`

        # Example 2: Search by first name and organization name
        `search_user_by(first_name="John", org_name="ExampleOrg")`
        """
        default_input_fields = {
            username: self.locators.USERNAME_INPUT,
            first_name: self.locators.FIRST_NAME_INPUT,
            last_name: self.locators.LAST_NAME_INPUT,
            email: self.locators.EMAIL_INPUT,
            org_name: self.locators.ORG_NAME_INPUT,
        }

        for value, locator in default_input_fields.items():
            # fill values only for filters specified in the function call
            if value:
                self.type_in_element_and_wait_for_spinner(locator, value)

    def set_status(self, active: Literal["ACTIVE", "INACTIVE"] = None):
        self.click_element(self.locators.STATUS_DROPDOWN)
        status = self.locators.STATUS_VALUE_OPTION.format(
            "ACTIVE" if active else "INACTIVE"
        )
        self.click_element(status)

    def reset_filters(self):
        self.click_element(self.locators.RESET_BUTTON)

    def click_on_user_email(self, email: str):
        self.click_element(
            self.locators.CELL_VALUE.format(email, UserFiltersCell.EMAIL.value)
        )

    def get_cell_element(
            self, filter_row_by: str, cell: UserFiltersCell, expected_cell_text: str
    ):
        return self.page.locator(
            self.locators.CELL_TEXT.format(
                filter_row_by, cell.value, expected_cell_text
            )
        )

    def return_resulting_rows(self):
        return self.page.locator(self.locators.RESULTING_ROWS)

    def get_total_visible_users(self):
        try:
            text = self.page.locator(self.locators.TOTAL_USER_COUNT).inner_text(timeout=5000)
            return int(text.split('of')[1].strip().split(" ")[0])
        except TimeoutError:
            logging.info("No resulting rows found")
            return 0
