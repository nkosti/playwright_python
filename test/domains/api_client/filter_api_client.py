from playwright.sync_api import Page

from test.domains.api_client.base_api_client import BaseApiClient


class FilterApiClient(BaseApiClient):
    def __init__(self, page: Page, env_data):
        super().__init__(page)
        self.req = page.request
        self.base_url = env_data["data-branching-service-url"]
        self.headers = {"Content-Type": "multipart/form-data"}

    ##continue
