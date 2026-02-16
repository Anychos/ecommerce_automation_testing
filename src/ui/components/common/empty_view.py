import allure
from playwright.sync_api import Page, expect

from src.ui.components.base import BaseComponent


class EmptyView(BaseComponent):
    """
    Компонент пустого состояния страницы
    """
    def __init__(self, page: Page, test_id_entity: str):
        super().__init__(page)

        self.root = self.page.get_by_test_id(f"empty-{test_id_entity}-message")

        self.icon = self.root.get_by_test_id(f"empty-{test_id_entity}-icon")
        self.title = self.root.get_by_test_id(f"empty-{test_id_entity}-title")
        self.text = self.root.get_by_test_id(f"empty-{test_id_entity}-text")

    @allure.step("Проверка видимости элементов пустого состояния")
    def check_visibility(self):
        expect(self.icon).to_be_visible()
        expect(self.title).to_be_visible()
        expect(self.text).to_be_visible()
