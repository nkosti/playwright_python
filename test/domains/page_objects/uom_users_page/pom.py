from playwright.sync_api import Page

from .create_user_page.pom import CreateUserPOM


class UsersPOM:
    def __init__(self, page: Page):
        self.page = page
        self.create_user = CreateUserPOM(page)