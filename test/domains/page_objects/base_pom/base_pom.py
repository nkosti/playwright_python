import logging

from playwright.sync_api import Page

from test import constants
from .locators import Locators


class BasePOM:
    def __init__(self, page: Page):
        self.page = page
        self.loc = Locators

    LOGGER = logging.getLogger(__name__)

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

    def return_successful_notification_element(self):
        return self.page.locator(self.loc.SUCCESSFUL_NOTIFICATION).last

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
