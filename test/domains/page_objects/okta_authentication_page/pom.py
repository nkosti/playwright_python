import os

from playwright.sync_api import Page

from test.domains.config.environments_handler import load_env_data
from test.domains.page_objects.base_pom.base_pom import BasePOM
from test.utils.utilities import Utilities
from .locators import Locators


class OktaAuthenticationPOM(BasePOM):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = Locators

    @staticmethod
    def return_env_data(data):
        if data:
            env_name = os.getenv("ENV_NAME") or "test"
            env_data = load_env_data(env_name)
            return env_data[data]
        return None

    def ciam_login(self, credentials=None):
        # Set default credentials
        default_username = "iam_username"
        default_password = "iam_password"

        # Override defaults with provided credentials
        if credentials:
            username, password, _ = credentials
        else:
            username = default_username
            password = default_password

        self.type_in_element(self.locators.IAM_USERNAME, self.return_env_data(username))
        #This is needed for supporting login to 11c staging. Delete when will stop using 2c
        if self.page.locator(self.locators.IAM_PASSWORD).is_hidden():
            self.click_element(self.locators.IAM_SIGN_IN)

        self.type_in_element(self.locators.IAM_PASSWORD, Utilities.decrypt_text(self.return_env_data(password)))
        self.click_element(self.locators.IAM_SIGN_IN)

    def new_user_login(self, username, password):
        self.type_in_element(self.locators.IAM_USERNAME, username)
        self.click_element(self.locators.IAM_SIGN_IN)
        self.type_in_element(self.locators.IAM_PASSWORD, password)
        self.click_element(self.locators.IAM_SIGN_IN)

    def set_new_password(self, password):
        self.type_in_element(self.locators.IAM_PASSWORD_NEW, password)
        self.type_in_element(self.locators.IAM_PASSWORD_CONFIRM, password)
        self.click_element(self.locators.SUBMIT_BUTTON)
