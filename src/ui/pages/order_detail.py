import re

from playwright.sync_api import Page, Locator, expect

from src.ui.pages.base import BasePage


class OrderDetailPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.icon = self.page.get_by_test_id("success-icon-symbol")
        self.title = self.page.get_by_test_id("success-title")
        self.order_id_text = self.page.get_by_test_id("order-number-title")
        self.order_id = self.page.get_by_test_id("order-number")
        self.date = self.page.get_by_test_id("order-date")
        self.cart_id = self.page.get_by_test_id("order-cart")
        self.what_next_text = self.page.get_by_test_id("steps-title")
        self.contact_text = self.page.get_by_test_id("contact-text")

    def step_title(self, index: int) -> Locator:
        return self.page.get_by_test_id(f"step-{index}-title")

    def step_description(self, index: int) -> Locator:
        return self.page.get_by_test_id(f"step-{index}-description")

    def button(self, test_id: str) -> Locator:
        return self.page.get_by_test_id(f"{test_id}-button")

    def check_visibility(self):
        expect(self.icon).to_be_visible()
        expect(self.title).to_be_visible()
        expect(self.title).to_have_text("Заказ успешно оформлен!")
        expect(self.order_id_text).to_be_visible()
        expect(self.order_id_text).to_have_text("Номер вашего заказа")
        expect(self.order_id).to_be_visible()
        expect(self.order_id).to_have_text(re.compile(r"#\d+"))
        expect(self.date).to_be_visible()
        expect(self.date).to_have_text(re.compile(r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}"))
        expect(self.cart_id).to_be_visible()
        expect(self.cart_id).to_have_text(re.compile(r"Создан\sиз\sкорзины\s#\d+"))

        expect(self.what_next_text).to_be_visible()
        expect(self.what_next_text).to_have_text("Что будет дальше?")

        expect(self.step_title(1)).to_be_visible()
        expect(self.step_title(1)).to_have_text("Подтверждение")
        expect(self.step_description(1)).to_be_visible()
        expect(self.step_description(1)).to_have_text("Мы свяжемся с вами для подтверждения заказа")

        expect(self.step_title(2)).to_be_visible()
        expect(self.step_title(2)).to_have_text("Обработка")
        expect(self.step_description(2)).to_be_visible()
        expect(self.step_description(2)).to_have_text("Заказ будет собран и подготовлен к отправке")

        expect(self.step_title(3)).to_be_visible()
        expect(self.step_title(3)).to_have_text("Доставка")
        expect(self.step_description(3)).to_be_visible()
        expect(self.step_description(3)).to_have_text("Курьер доставит заказ по указанному адресу")

        expect(self.button("view-orders")).to_be_visible()
        expect(self.button("view-orders")).to_have_text("Перейти к моим заказам")
        expect(self.button("continue-shopping")).to_be_visible()
        expect(self.button("continue-shopping")).to_have_text("Продолжить покупки")

        expect(self.contact_text).to_be_visible()
        expect(self.contact_text).to_have_text("Вопросы по заказу?")

        expect(self.button("phone")).to_be_visible()
        expect(self.button("phone")).to_have_text("8-800-123-45-67")
        expect(self.button("email")).to_be_visible()
        expect(self.button("email")).to_have_text("support@example.com")

    def click_button(self, test_id: str):
        expect(self.button(test_id)).to_be_visible()
        self.button(test_id).click()




