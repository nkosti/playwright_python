from playwright.sync_api import Page

from test import constants
from .locators import Locators


class BasePOM:
    def __init__(self, page: Page):
        self.page = page
        self.loc = Locators

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
