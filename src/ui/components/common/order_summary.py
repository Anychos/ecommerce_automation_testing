import re

from playwright.sync_api import Page, Locator, expect

from src.ui.components.base import BaseComponent


class OrderSummary(BaseComponent):
    def __init__(self, page: Page, root: Locator):
        super().__init__(page)

        self.root = root

        self.delivery_info_container = self.page.get_by_test_id("delivery-info")
        self.delivery_info_text = self.delivery_info_container.get_by_test_id("delivery-info-text")

        self.order_item_row = self.root.locator("[data-testid^=order-item-row-]").first
        self.order_item_name = self.order_item_row.locator("[data-testid^=order-item-name-]")
        self.order_item_details = self.order_item_row.locator("[data-testid^=order-item-details-]")
        self.order_item_total_price = self.order_item_row.locator("[data-testid^=order-item-total-]")

    def title(self, test_id: str) -> Locator:
        return self.root.get_by_test_id(f"{test_id}-title")

    def label(self, test_id: str) -> Locator:
        return self.root.get_by_test_id(f"{test_id}-label")

    def label_value(self, test_id: str) -> Locator:
        return self.root.get_by_test_id(f"{test_id}-value")

    def button(self, test_id: str) -> Locator:
        return self.root.get_by_test_id(f"{test_id}-button")

    def check_visibility(self, *, page_name: str, is_free_delivery: bool = False):
        if page_name == "cart":
            expect(self.title("summary")).to_be_visible()
            expect(self.title("summary")).to_have_text("Итого")

            expect(self.label("subtotal")).to_be_visible()
            expect(self.label("subtotal")).to_have_text(re.compile(r"Товары\s\(\d+\)"))
            expect(self.label_value("subtotal")).to_be_visible()
            expect(self.label_value("subtotal")).to_have_text(re.compile(r"\d+\.\d+\s₽"))

            expect(self.label("delivery")).to_be_visible()
            expect(self.label("delivery")).to_have_text("Доставка")
            expect(self.label_value("delivery")).to_be_visible()

            expect(self.label("total")).to_be_visible()
            expect(self.label("total")).to_have_text("К оплате")
            expect(self.label_value("total")).to_be_visible()
            expect(self.label_value("total")).to_have_text(re.compile(r"\d+\.\d+\s₽"))

            if is_free_delivery:
                expect(self.delivery_info_container).to_be_visible()
                expect(self.delivery_info_text).to_have_text(re.compile(r"Добавьте товаров на \d+\.\d+\s₽ для бесплатной доставки"))
            else:
                expect(self.label_value("delivery")).to_have_text(re.compile(r"\d+\s₽"))
                expect(self.delivery_info_container).to_be_visible()
                expect(self.delivery_info_text).to_be_visible()
                expect(self.delivery_info_text).to_have_text(re.compile(r"Добавьте товаров на \d+\.\d+\s₽ для бесплатной доставки"))

            expect(self.button("checkout")).to_be_visible()
            expect(self.button("checkout")).to_have_text("Оформить заказ")
            expect(self.button("continue-shopping")).to_be_visible()
            expect(self.button("continue-shopping")).to_have_text("Продолжить покупки")

        elif page_name == "checkout":
            expect(self.title("summary")).to_be_visible()
            expect(self.title("summary")).to_have_text("Ваш заказ")

            expect(self.label("cart-number")).to_be_visible()
            expect(self.label("cart-number")).to_have_text("Корзина:")
            expect(self.label_value("cart-number")).to_be_visible()
            expect(self.label_value("cart-number")).to_have_text(re.compile(r"#\d+"))

            expect(self.label("cart-items")).to_be_visible()
            expect(self.label("cart-items")).to_have_text("Товаров:")
            expect(self.label_value("cart-items")).to_be_visible()
            expect(self.label_value("cart-items")).to_have_text(re.compile(r"\d+\sшт\."))

            expect(self.title("items")).to_be_visible()
            expect(self.title("items")).to_have_text("Состав заказа:")

            expect(self.order_item_name).to_be_visible()
            expect(self.order_item_details).to_be_visible()
            expect(self.order_item_details).to_have_text(re.compile(r"\d+\s×\s\d+\.\d+\s₽"))
            expect(self.order_item_total_price).to_be_visible()
            expect(self.order_item_total_price).to_have_text(re.compile(r"\d+\.\d+\s₽"))

            expect(self.label("subtotal")).to_be_visible()
            expect(self.label("subtotal")).to_have_text("Товары")
            expect(self.label_value("subtotal")).to_be_visible()
            expect(self.label_value("subtotal")).to_have_text(re.compile(r"\d+\.\d+\s₽"))

            expect(self.label("delivery")).to_be_visible()
            expect(self.label("delivery")).to_have_text("Доставка")
            expect(self.label_value("delivery")).to_be_visible()

            if is_free_delivery:
                expect(self.label_value("delivery")).to_have_text("Бесплатно")
            else:
                expect(self.label_value("delivery")).to_have_text("100 ₽")

            expect(self.label("total")).to_be_visible()
            expect(self.label("total")).to_have_text("Итого к оплате")
            expect(self.label_value("total")).to_be_visible()
            expect(self.label_value("total")).to_have_text(re.compile(r"\d+\.\d+\s₽"))

            expect(self.button("place-order")).to_be_visible()
            expect(self.button("place-order")).to_have_text("Подтвердить заказ")
            expect(self.button("back-to-cart")).to_be_visible()
            expect(self.button("back-to-cart")).to_have_text("Вернуться в корзину")

    def click_button(self, test_id: str):
        expect(self.button(test_id)).to_be_visible()
        self.button(test_id).click()
