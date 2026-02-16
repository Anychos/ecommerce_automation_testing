import re

import allure
from playwright.sync_api import Page, expect


class BasePage:
    """
    Базовый класс для работы со страницами
    """
    def __init__ (self, page: Page):

        self.page = page

    @allure.step("Открытие страницы {url}")
    def open_url(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded")

    @allure.step("Перезагрузка страницы")
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

    @allure.step("Проверка что URL содержит {value}")
    def check_url_contains(self, value: str):
        self.check_current_url(value)

    @allure.step("Проверка что URL соответствует {value}")
    def check_url_exact(self, value: str):
        self.check_current_url(value, exact=True)

    @allure.step("Проверка что URL соответствует паттерну {pattern}")
    def check_url_matches(self, pattern: re.Pattern):
        self.check_current_url(pattern)

