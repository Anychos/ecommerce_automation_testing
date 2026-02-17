import re

import allure
from playwright.sync_api import Page, expect

from src.ui.components.base import BaseComponent


class OrderItem(BaseComponent):
    """
    Компонент элемента заказа в списке заказов
    """

    def __init__(self, page: Page):
        super().__init__(page)

        self.root = self.page.locator("[data-testid^=order-row-]").first

        self.order_id = self.root.get_by_test_id("order-number")
        self.date = self.root.get_by_test_id("raw-date")
        self.cart_id = self.root.get_by_test_id("cart-badge")
        self.status = self.root.get_by_test_id("default-status-badge")
        self.detail_button = self.root.locator("[data-testid^=view-order-button-]")

    @allure.step("Проверка видимости элементов заказа в списке заказов")
    def check_visibility(self) -> None:
        """
        Проверяет видимость элементов заказа в списке заказов
        """

        expect(self.order_id).to_be_visible()
        expect(self.order_id).to_have_text(re.compile(r"#\d+"))
        expect(self.date).to_be_visible()
        expect(self.date).to_have_text(re.compile(r"\d{4}-\d{2}-\d{2}"))
        expect(self.cart_id).to_be_visible()
        expect(self.cart_id).to_have_text(re.compile(r"Корзина\s#\d+"))
        expect(self.status).to_be_visible()
        expect(self.detail_button).to_be_visible()
        expect(self.detail_button).to_have_text("Просмотр")

    @allure.step("Клик по кнопке просмотра заказа")
    def click_detail_button(self) -> None:
        """
        Кликает по кнопке просмотра заказа
        """

        expect(self.detail_button).to_be_visible()
        self.detail_button.click()
