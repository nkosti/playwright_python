import logging
from typing import List

from playwright.sync_api import Page

from test.domains.page_objects.base_pom.base_pom import BasePOM
from .locators import Locators


class CreateUserPOM(BasePOM):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = Locators
        self.page = page

    def fill_user_info(
            self,
            first_name: str = None,
            last_name: str = None,
            email: str = None,
            phone: str = None,
            notam_office: str = None,
    ):
        default_input_fields = {
            first_name: self.locators.FIRST_NAME_INPUT,
            last_name: self.locators.LAST_NAME_INPUT,
            email: self.locators.EMAIL_INPUT,
            phone: self.locators.PHONE_INPUT,
            notam_office: self.locators.NOTAM_OFFICE,
        }

        for value, locator in default_input_fields.items():
            # fill values only for fields specified in the function call
            if value:
                self.type_in_element(locator, value)

    def set_organization(self, org_name: str = None):
        if org_name:
            self.click_element(self.locators.ORG_NAME_MENU)
            self.type_in_element(self.locators.ORG_NAME_INPUT, org_name)
            self.waiting_for_spinner()
            self.click_element(self.locators.ORG_NAME_OPTION.format(org_name.upper()))

    def set_user_roles(self, user_roles: dict):
        if user_roles:
            for key, value in user_roles.items():
                self.page.get_by_label(key, exact=True).set_checked(checked=value)

    def close_user_window(self):
        self.click_element(self.locators.CLOSE_BUTTON)

    def activate_user(self):
        self.click_element(self.locators.ACTIVATE_BUTTON)
        self.click_element(self.locators.CONFIRM_ACTIVATE_BUTTON)

    def deactivate_user(self):
        self.click_element(self.locators.DEACTIVATE_BUTTON)
        self.click_element(self.locators.CONFIRM_DEACTIVATE_BUTTON)

    def edit_user_details(self):
        self.click_element(self.locators.EDIT_USER_BUTTON)

    def save_user_settings(self):
        self.click_element(self.locators.SAVE_BUTTON)

    def save_updated_user_settings(self):
        self.click_element(self.locators.SAVE_UPDATED_USER_BUTTON)

    def all_roles_are_unassigned(self):
        return len(self.page.query_selector_all("input[type=checkbox]:checked")) == 0

    def get_all_assigned_roles(self) -> List[str]:
        """
        Scans all checkboxes and returns a list of text values from the span element for the checked ones.
        """
        self.page.wait_for_timeout(5000)
        checked_roles = self.page.locator(
            self.locators.GENERIC_CHECKED_ROLE
        ).all_inner_texts()

        logging.info(f"Assigned roles: {checked_roles}")

        return checked_roles

    def close_popup(self):
        self.click_element(self.locators.CLOSE_MESSAGE_POPUP_BUTTON)

    def return_first_name_element(self):
        return self.page.locator(self.locators.FIRST_NAME_INPUT)

    def return_last_name_element(self):
        return self.page.locator(self.locators.LAST_NAME_INPUT)

    def return_email_element(self):
        return self.page.locator(self.locators.EMAIL_INPUT)

    def return_phone_element(self):
        return self.page.locator(self.locators.PHONE_INPUT)

    def return_notam_office_element(self):
        return self.page.locator(self.locators.NOTAM_OFFICE)

    def return_org_name_saved_element(self):
        return self.page.locator(self.locators.ORG_NAME_SAVED)
