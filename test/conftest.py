import json
import logging
import os
import sys

import allure
import pytest
from _pytest.config import Config
from _pytest.nodes import Item
from playwright.sync_api import Page
from slugify import slugify

from test import constants
from test.domains.api_client.filter_api_client import FilterApiClient
from test.domains.config.environments_handler import load_env_data
from test.domains.page_objects.base_pom.base_pom import BasePOM
from test.domains.page_objects.landing_page.pom import LandingPagePOM
from test.domains.page_objects.uom_organizations_page.pom import OrganizationsPOM
from test.domains.page_objects.uom_users_page.pom import UsersPOM
from test.domains.test_data.dto.users.users_dto import UserDTO
from test.skipped_tests_config import skipped_tests
from test.utils.utilities import Utilities


class Context:
    DOWNLOADED_FOLDER = constants.DOWNLOADED_FOLDER

    def __init__(self, page: Page):
        # init page objects here
        self.page = page
        self.basePOM = BasePOM(page)
        self.landing_pom = LandingPagePOM(page)
        self.organizations = OrganizationsPOM(page)
        self.users = UsersPOM(page)

class ApiContext:
    def __init__(self, page: Page, env_data):
        self.data_branching_api_client = FilterApiClient(page, env_data)


@pytest.fixture
def api_clients(page, env_data):
    return ApiContext(page, env_data)


@pytest.fixture()
def browser_context_args(
        browser_context_args, tmpdir_factory: pytest.TempdirFactory, env_data
):
    return {
        **browser_context_args,
        "record_video_dir": tmpdir_factory.mktemp("videos"),
        "ignore_https_errors": True,
        "base_url": env_data["base_url"],
        "viewport": {"width": 1920, "height": 1080}
    }


@pytest.fixture()
def downloaded_folder():
    return constants.DOWNLOADED_FOLDER


@pytest.fixture
def env_data():
    env_name = os.getenv("ENV_NAME") or "test"
    return load_env_data(env_name)


@pytest.fixture()
def json_data(request):
    json_file_path = os.path.join(
        "test",
        "resources",
        "test_data",
        Utilities.get_test_number(request).strip() + ".json",
    )

    try:
        with open(json_file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error while parsing json file:{json_file_path} with error: {e}")


@pytest.fixture(scope="function", autouse=True)
def log_test_name_at_start(request):
    """
    Before starting a test, log its name.
    This makes it easier to retrieve the logs for a specific test.
    """
    logging.info("=" * 20 + request.node.nodeid + "=" * 20)


@pytest.fixture
def poms(page):
    return Context(page)


def pytest_cmdline_main(config: Config):
    # hooks to read the allure dir from command line so to use them in After Suite hooks
    command_line_allure_dir = config.known_args_namespace.allure_report_dir
    if command_line_allure_dir is not None:
        constants.ALLURE_DIR = command_line_allure_dir


def pytest_configure():
    """
    Configures pytest logging to output each worker's log messages
    to its own worker log file and to the console.
    """
    # Determine worker id
    # Also see: https://pytest-xdist.readthedocs.io/en/latest/how-to.html#creating-one-log-file-for-each-worker
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", default="gw0")

    # Create logs folder
    logs_folder = os.environ.get("LOGS_FOLDER", default="logs_folder")
    os.makedirs(logs_folder, exist_ok=True)

    # Create file handler to output logs into corresponding worker file
    file_handler = logging.FileHandler(
        f"{logs_folder}/logs_worker_{worker_id}.log", mode="w"
    )
    file_handler.setFormatter(
        logging.Formatter(
            fmt="{asctime} {levelname}:{name}:{lineno}:{message}",
            style="{",
        )
    )

    # Create stream handler to output logs on console
    # This is a workaround for a known limitation:
    # https://pytest-xdist.readthedocs.io/en/latest/known-limitations.html
    console_handler = logging.StreamHandler(sys.stderr)  # pytest only prints error logs
    console_handler.setFormatter(
        logging.Formatter(
            # Include worker id in log messages, \r is needed to separate lines in console
            fmt="\r{asctime} " + worker_id + ":{levelname}:{name}:{lineno}:{message}",
            style="{",
        )
    )

    # Configure logging
    logging.basicConfig(level=logging.INFO, handlers=[console_handler, file_handler])


def pytest_bdd_before_scenario(request, feature, scenario):
    should_skip = any(tag.strip() in skipped_tests for tag in scenario.tags)

    if should_skip:
        pytest.skip(
            f"Scenario '{scenario.name}' is skipped because: {skipped_tests.get(list(scenario.tags)[0].strip())}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call):
    outcome = yield
    result = outcome.get_result()

    # Check if allure is being used
    check_str = "--alluredir"
    try:
        # This is how we get access in arguments when tests are run in parallel with xdist
        dict_argv_ = item.funcargs["request"].config.workerinput["mainargv"]
    except Exception:
        dict_argv_ = sys.argv

    res = any(check_str in sub for sub in dict_argv_)

    if call.when == "call" and result.failed and res:
        if item.funcargs["request"].getfixturevalue("page"):
            page: Page = item.funcargs["request"].getfixturevalue("page")
            page = page.context.pages.pop()
            logging.info("Attaching screenshot to Allure report...")
            allure.attach(
                page.screenshot(type="png", full_page=True),
                name=f"{slugify(item.nodeid)}.png",
                attachment_type=allure.attachment_type.PNG,
            )
            logging.info("Screenshot successfully attached to Allure report.")

            try:
                video_path = page.video.path()
                page.context.close()  # ensure video saved

                if video_path:
                    logging.info("Attaching video to Allure report...")
                    video_stream = open(video_path, "rb")
                    video_data = video_stream.read()
                    allure.attach(
                        video_data,
                        name=f"{slugify(item.nodeid)}.webm",
                        attachment_type=allure.attachment_type.WEBM,
                    )
                    video_stream.close()
                    logging.info("Video successfully attached to Allure report.")
            except Exception as e:
                logging.error(f"Couldn't save video! \n Original exception: {e}")


@pytest.fixture()
def user_dto(json_data):
    return UserDTO(json_data["User"][0])


@pytest.fixture()
def second_user_dto(json_data):
    return UserDTO(json_data["User"][1])


class EnvData:
    """
    Store dynamic data, retrievable by API, that is different across environments.
    """
    roles = {}
    orgs = {}
