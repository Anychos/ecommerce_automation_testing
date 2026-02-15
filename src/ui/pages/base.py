import re

from playwright.sync_api import Page, expect

from config import settings
from src.ui.tools.routes import Route


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

    def check_current_url(
        self,
        expected: str | re.Pattern,
        *,
        exact: bool = False,
        timeout: int = 5000
    ) -> None:
        """
        Проверяет текущий URL страницы

        :param expected:
            - str → проверка по contains (по умолчанию)
            - re.Pattern → проверка по regex
        :param exact:
            Если True и expected=str → полное совпадение URL
        :param timeout: Время ожидания загрузки страницы
        """

        if isinstance(expected, re.Pattern):
            expect(self.page).to_have_url(expected, timeout=timeout)

        elif exact:
            expect(self.page).to_have_url(expected, timeout=timeout)

        else:
            expect(self.page).to_have_url(
                re.compile(re.escape(expected)),
                timeout=timeout
            )

    def check_url_contains(self, value: str):
        self.check_current_url(value)

    def check_url_exact(self, value: str):
        self.check_current_url(value, exact=True)

    def check_url_matches(self, pattern: re.Pattern):
        self.check_current_url(pattern)

