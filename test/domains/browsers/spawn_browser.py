from playwright.sync_api import Browser


def get_new_page(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    return page


def get_new_context(browser: Browser):
    return browser.new_context()
