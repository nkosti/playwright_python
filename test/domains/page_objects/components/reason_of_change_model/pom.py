from playwright.sync_api import Page

from test.domains.page_objects.base_pom.base_pom import BasePOM
from test.domains.page_objects.components.reason_of_change_model.locators import Locators


class ReasonOfChangeComponentPOM(BasePOM):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = Locators

    def input_reason_of_change(self, message: str, wait_for_toast_message_to_be_visible: bool = True,
                               wait_for_toast_message_to_be_hidden: bool = True):
        self.type_in_element(self.locators.INPUT_REASON_OF_CHANGE, message)
        self.click_element(self.locators.CONFIRM_MODAL_BUTTON)
        if wait_for_toast_message_to_be_visible:
            self.return_toast_message_element().wait_for(state='visible')
        if wait_for_toast_message_to_be_hidden:
            self.return_toast_message_element().wait_for(state='hidden')
