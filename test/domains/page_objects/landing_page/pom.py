from playwright.sync_api import Page

from test.domains.page_objects.base_pom.base_pom import BasePOM
from .locators import Locators


class LandingPagePOM(BasePOM):
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = Locators()

    def open_landing_page(self):
        self.page.goto("fe/cmm/parent-app")

    def _open_app(self, app_locator):
        """
        Opens an app by clicking on the header and the app name
        """
        self.open_home_page()
        self.click_element(self.locators.MENU_BTN)
        self.click_element(app_locator)

    def _open_sub_app(self, page_name: str):
        self.click_element(self.locators.SUB_MENU.format(page_name))

    def open_home_page(self):
        self.click_element(self.locators.HOME_BTN)

    def open_uom(self):
        self._open_app(self.locators.UOM)

    def open_users(self):
        self.open_uom()
        self.click_element(self.locators.USERS)

    def open_organizations(self):
        self.open_uom()
        self.click_element(self.locators.ORGANIZATIONS)

    def open_user_profile(self):
        self.click_element(self.locators.USER_PROFILE_BTN)

    def sign_out(self):
        self.open_user_profile()
        self.click_element(self.locators.LOGOUT_BTN)
