import re

from playwright.sync_api import Page, Locator, expect

from src.ui.components.common.empty_view import EmptyView
from src.ui.components.orders_list_page.order_item import OrderItem
from src.ui.pages.base import BasePage


class OrdersPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.page_title = self.page.get_by_test_id("orders-title")
        self.orders_counter_text = self.page.get_by_test_id("orders-count")
        self.last_updated_text = self.page.get_by_test_id("last-updated")

        self.order_item = OrderItem(self.page)

        self.empty_view = EmptyView(self.page, "orders")
        self.start_shopping_button = self.page.get_by_test_id("start-shopping-button")

    def column_name(self, test_id: str) -> Locator:
        return self.page.get_by_test_id(f"order-{test_id}-header")

    def check_visibility(self, *, is_empty: bool = False):
        expect(self.page_title).to_be_visible()
        expect(self.page_title).to_have_text("Мои заказы")

        if is_empty:
            self.empty_view.check_visibility()
            expect(self.start_shopping_button).to_be_visible()
            expect(self.start_shopping_button).to_have_text("Начать покупки")
        else:
            expect(self.orders_counter_text).to_be_visible()
            expect(self.orders_counter_text).to_have_text(re.compile(r"Всего заказов:\s\d+"))
            expect(self.last_updated_text).to_be_visible()

            expect(self.column_name("id")).to_be_visible()
            expect(self.column_name("id")).to_have_text("№ Заказа")
            expect(self.column_name("date")).to_be_visible()
            expect(self.column_name("date")).to_have_text("Дата")
            expect(self.column_name("cart")).to_be_visible()
            expect(self.column_name("cart")).to_have_text("Корзина")
            expect(self.column_name("status")).to_be_visible()
            expect(self.column_name("status")).to_have_text("Статус")
            expect(self.column_name("actions")).to_be_visible()
            expect(self.column_name("actions")).to_have_text("Действия")

            self.order_item.check_visibility()



