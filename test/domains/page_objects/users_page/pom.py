from playwright.sync_api import Page

from .create_user_page.pom import CreateUserPOM
from .find_users_page.pom import FindUserPOM
from ..components.reason_of_change_model.pom import ReasonOfChangeComponentPOM


class UsersPOM:
    def __init__(self, page: Page):
        self.page = page
        self.find_user = FindUserPOM(page)
        self.create_user = CreateUserPOM(page)
        self.reason_of_change_component = ReasonOfChangeComponentPOM(page)
