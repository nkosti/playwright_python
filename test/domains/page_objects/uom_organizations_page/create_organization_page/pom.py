from playwright.sync_api import Page

from test.domains.page_objects.base_pom.base_pom import BasePOM
from .locators import Locators


class CreateOrganizationPOM(BasePOM):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = Locators
        self.page = page

    def input_organization_name(self, name: str):
        self.type_in_element(self.locators.ORGANIZATION_NAME, name)

    def input_organization_city(self, city: str):
        self.type_in_element(self.locators.ORGANIZATION_CITY, city)

    def click_save_button(self):
        self.click_element(self.locators.SAVE_BUTTON)
