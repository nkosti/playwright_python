from test.domains.page_objects.base_pom.base_pom import BasePOM

from .locators import Locators


class FindOrganizationPOM(BasePOM):

    def click_create_button(self):
        self.click_element(self.locators.CREATE_BUTTON)
