import logging
import os
from typing import Literal

from playwright.sync_api import Page, TimeoutError

from test import constants
from .locators import Locators


class BasePOM:
    def __init__(self, page: Page):
        self.page = page
        self.loc = Locators

    LOGGER = logging.getLogger(__name__)

    def click_element(self, locator: str, time_out: float = 30_000):
        try:
            self.page.locator(locator).click(timeout=time_out)
            self.LOGGER.info(f"Click element : {locator}")
        except Exception as e:
            raise Exception(
                f"Element with locator: {locator} could not be clicked.\n Original exception: {e}"
            )

    def click_element_in_frame(
            self, locator: str, frame_loc: str, time_out: float = 30_000
    ):
        try:
            self.page.frame_locator(frame_loc).locator(locator).click(timeout=time_out)
            self.LOGGER.info(f"Click element : {locator}")
        except Exception as e:
            raise Exception(
                f"Element with locator: {locator} could not be clicked.\n Original exception: {e}"
            )

    def type_in_element(self, locator: str, text: str, press_enter=False):
        try:
            self.page.locator(locator).fill(text)
            self.LOGGER.info(f"Type in element : {locator} text : {text}")
            if press_enter:
                self.page.locator(locator).press("Enter")
        except Exception as e:
            raise Exception(
                f"Cannot write {text} in element with locator {locator}. \n Original exception: {e}"
            )

    def type_in_element_in_frame(
            self, locator: str, frame_loc: str, text: str, press_enter=False
    ):
        try:
            self.page.frame_locator(frame_loc).locator(locator).fill(text)
            self.LOGGER.info(f"Type in element : {locator} text : {text}")
            if press_enter:
                self.page.locator(locator).press("Enter")
        except Exception as e:
            raise Exception(
                f"Cannot write {text} in element with locator {locator}. \n Original exception: {e}"
            )

    def type_in_element_and_wait_for_spinner(self, locator: str, text: str):
        self.type_in_element(locator, text, True)
        self.waiting_for_spinner()

    def set_checked(self, locator: str, checked: bool):
        self.page.locator(locator).set_checked(checked)

    def waiting_for_spinner(
            self, timeout=3, spinner_element=Locators.SPINNER_ELEMENT
    ):
        """
        Waits for the loading spinner to appear and disappear.
        If the spinner does not appear, the method continues without failing.

        :param poms: Context object that acts as a Page Factory and context manager.
        :param timeout: Maximum time to wait for the spinner to appear, in seconds.
        :param spinner_element: Spinner element can be provided if different from the base element.
        """

        try:
            # Wait for the spinner to appear with a timeout
            # To appear normally will not want more than 3 seconds
            self.page.locator(spinner_element).wait_for(
                state="visible", timeout=timeout * 1000
            )
            # If spinner appears, wait for it to disappear
            # The spinner could take longer to disappear so removing the timeout and implicitly take the default 30 sec
            self.page.locator(spinner_element).wait_for(state="hidden")
        except Exception as e:
            self.LOGGER.info(
                f"Exception throw in waiting_for_loading_the_result function"
            )
            # If spinner does not appear, or any other exception occurs, continue without failing
            pass

    def get_attribute(self, locator: str, attribute: str) -> str:
        try:
            attr = self.page.locator(locator).get_attribute(attribute)
            return attr
        except Exception as e:
            raise Exception(
                f"Cannot get attribute: {attribute} in element with locator {locator}. \n Original exception: {e}"
            )

    def get_text(self, locator: str) -> str:
        try:
            attr = self.page.locator(locator).text_content()
            return attr
        except Exception as e:
            raise Exception(
                f"Cannot get text content in element with locator {locator}. \n Original exception: {e}"
            )

    def upload_files(self, locator: str, file: str):
        try:
            mime_types = {
                "default": "text/plain",
                "csv": "text/csv",
                "json": "application/json",
                "xml": "application/xml",
                "xls": "application/vnd.ms-excel",
                "xslt": "text/xml",
                "zip": "application/zip",
                "jpg": "image/jpeg",
            }
            with open(file, "rb") as f:
                file_content = f.read()

            file_name = os.path.basename(file)
            file_extension = file_name.split(".")[1]
            mime = mime_types.get(file_extension, mime_types["default"])

            self.page.locator(locator).set_input_files(
                files=[{"name": file_name, "mimeType": mime, "buffer": file_content}]
            )

            logging.info(f"Using locator {locator} uploading file {file} ")
        except Exception as e:
            raise Exception(
                f"Cannot upload files {file} in element with locator {locator}. \n Original exception: {e}"
            )

    def download_file(
            self,
            loc,
            folder_to_download: str = constants.DOWNLOADED_FOLDER,
            timeout: float = 30_000,
    ) -> str:
        """
        This function downloads the file in target directory, the directory that output of the build files should use.
        :param loc: The web download element or its locator
        :param folder_to_download:
        :param timeout:
        :return: the downloaded file path
        """
        with self.page.expect_download() as download_info:
            if isinstance(loc, str):
                loc = self.page.locator(loc)
            loc.click(timeout=timeout)

        download = download_info.value

        dir_to_save = os.path.join(folder_to_download, download.suggested_filename)

        download.save_as(dir_to_save)

        return dir_to_save

    def close_notification(self, timeout: float = 3_000):
        try:
            self.click_element(self.loc.CLOSE_MESSAGE_POPUP_BUTTON, time_out=timeout)
        except Exception as e:
            logging.info(f"Notification not appeared: {e}")

    def close_notification_contains_text(self, text: str, timeout: float = 3_000):
        try:
            self.click_element(self.loc.CLOSE_NOTIFICATION_WITH_TEXT.format(text), time_out=timeout)
        except Exception as e:
            logging.info(f"Notification not appeared: {e}")

    def return_successful_notification_element(self):
        return self.page.locator(self.loc.SUCCESSFUL_NOTIFICATION).last

    def return_toast_message_element(self, selection="last"):
        if selection == "first":
            return self.page.locator(self.loc.TOAST_MESSAGE).first
        elif selection == "last":
            return self.page.locator(self.loc.TOAST_MESSAGE).last
        else:
            raise ValueError("Invalid selection. Choose 'first' or 'last'.")

    def return_toast_message_element_with_text(self, text: str):
        return self.page.locator(self.loc.TOAST_MESSAGE_WITH_TEXT.format(text))

    '''
        Handle the case when test select from 2 dropdown menu sequentially and contains common option.
        e.g select1 has option [A, B, C] and select2 [C, D, E], when you select something from select1 and you open select2
        to select C, playwright throw error because it finds 2 items that has-text("C") since options from select1 is still visible 
    '''

    def element_is(self, locator: str,
                   state: Literal["attached", "detached", "hidden", "visible"] | None = None,
                   timeout: float | None = 5000) -> bool:
        try:
            self.page.locator(locator).wait_for(state=state, timeout=timeout)
            return True
        except TimeoutError:
            return False

    '''
    Function that return all attributes from matched element in a list
    Take as parameter the locator that matches all elements and looping using nth gets
    the attribute value and append it to a list
    '''

    def get_elements_attribute(self, loc: str, attribute: str):
        result = []
        for i in range(self.page.locator(loc).count()):
            result.append(self.page.locator(f'{loc}>>nth={i}').get_attribute(attribute))

        return result
