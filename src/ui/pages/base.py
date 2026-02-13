import re

from playwright.sync_api import Page, expect


class BasePage:
    """
    Базовый класс для работы со страницами
    """
    def __init__ (self, page: Page):

        self.page = page

    def open_url(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded")

    def reload_page(self):
        self.page.reload(wait_until="domcontentloaded")

    def check_current_page_url(self, navigation_path: str):
        expect(self.page).to_have_url(
            re.compile(rf".*/{navigation_path}*")
        )
