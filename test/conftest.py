import pytest

from test import constants
from test.skipped_tests_config import skipped_tests


class Context:
    DOWNLOADED_FOLDER = constants.DOWNLOADED_FOLDER


@pytest.fixture()
def downloaded_folder():
    return constants.DOWNLOADED_FOLDER


def pytest_bdd_before_scenario(request, feature, scenario):
    should_skip = any(tag.strip() in skipped_tests for tag in scenario.tags)

    if should_skip:
        pytest.skip(
            f"Scenario '{scenario.name}' is skipped because: {skipped_tests.get(list(scenario.tags)[0].strip())}")
