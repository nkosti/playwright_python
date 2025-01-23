import pytest
from playwright.sync_api import Page

from test import constants
from test.domains.page_objects.base_pom.base_pom import BasePOM
from test.skipped_tests_config import skipped_tests


class Context:
    DOWNLOADED_FOLDER = constants.DOWNLOADED_FOLDER

    def __init__(self, page: Page):
        # init page objects here
        self.page = page
        self.basePOM = BasePOM(page)


class ApiContext:
    def __init__(self, page: Page, env_data):
        self.data_branching_api_client = DataBranchingApiClient(page, env_data)



@pytest.fixture()
def downloaded_folder():
    return constants.DOWNLOADED_FOLDER


@pytest.fixture
def poms(page):
    return Context(page)


def pytest_bdd_before_scenario(request, feature, scenario):
    should_skip = any(tag.strip() in skipped_tests for tag in scenario.tags)

    if should_skip:
        pytest.skip(
            f"Scenario '{scenario.name}' is skipped because: {skipped_tests.get(list(scenario.tags)[0].strip())}")
