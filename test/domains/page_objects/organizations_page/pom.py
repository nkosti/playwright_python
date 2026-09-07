from playwright.sync_api import Page

from .create_organization_page.pom import CreateOrganizationPOM
from .find_organization_page.pom import FindOrganizationPOM


class OrganizationsPOM:
    def __init__(self, page: Page):
        self.page = page
        self.find_organization = FindOrganizationPOM(page)
        self.create_organization = CreateOrganizationPOM(page)
