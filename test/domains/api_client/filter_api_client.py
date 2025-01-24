from playwright.sync_api import Page

from test.domains.api_client.base_api_client import BaseApiClient
from test.domains.enum.api.filter_endpoints.endpoints import FiltersEndpoint


class FilterApiClient(BaseApiClient):
    def __init__(self, page: Page, env_data):
        super().__init__(page)
        self.req = page.request
        self.base_url = env_data["data-branching-service-url"]
        self.headers = {"Content-Type": "multipart/form-data"}

    def filter_by(self, filter_by):
        return self.get(FiltersEndpoint.REPORT.value.format(filter_by))

    def retrieve_detailed_action_report(self, filter_by, severity: SeverityTypes):
        return self.get(
            FiltersEndpoint.DETAILED_REPORT.value.format(filter_by, severity.value)
        )
