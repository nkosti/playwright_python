from urllib.parse import urljoin

from playwright.sync_api import Page


class BaseApiClient:

    def __init__(self, page: Page):
        self.client = page.context.request
        self.base_url = ""

    def get(self, resource_url: str, data=None, headers=None):
        return self.client.get(self.url(resource_url), data=data, headers=headers)

    def post(self, resource_url: str, data=None, headers=None):

        return self.client.post(self.url(resource_url), data=data, headers=headers)

    def url(self, resource_url: str):
        return urljoin(self.base_url, resource_url)
