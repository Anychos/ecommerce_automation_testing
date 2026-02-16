import allure
from playwright.sync_api import Page, expect

from src.ui.components.common.empty_view import EmptyView
from src.ui.components.common.footer import Footer
from src.ui.components.common.header import Header
from src.ui.components.home_page.product_card import ProductCard
from src.ui.pages.base import BasePage


class HomePage(BasePage):
    """
    Класс главной страницы
    """
    def __init__(self, page: Page):
        super().__init__(page)

        self.header = Header(self.page)

        self.success_message = self.page.get_by_test_id("flash-message-success")
        self.success_logout_message = self.page.get_by_test_id("flash-message-info")

        self.hero_title = self.page.get_by_test_id("main-title")
        self.hero_text = self.page.get_by_test_id("main-subtitle")

        self.products_list_title = self.page.get_by_test_id("products-title")
        self.empty_list_view = EmptyView(self.page, "products")

        self.footer = Footer(self.page)

    def get_product_card(self, product_id: int) -> ProductCard:
        return ProductCard(self.page, product_id)

    def add_to_cart_notification(self, alert_type: str):
        return self.page.locator(f".alert-{alert_type}").first

    @allure.step("Проверка видимости элементов главной страницы")
    def check_visibility(self, *, is_empty: bool = False):
        expect(self.hero_title).to_be_visible()
        expect(self.hero_text).to_be_visible()

        expect(self.products_list_title).to_be_visible()
        expect(self.products_list_title).to_have_text("Товары")

        if is_empty:
            self.empty_list_view.check_visibility()
        else:
            self.get_product_card(1).check_visibility()

    @allure.step("Проверка нотификации успешной регистрации")
    def check_success_registration_message(self):
        expect(self.success_message).to_be_visible()
        expect(self.success_message).to_have_text("Регистрация успешна!")

    @allure.step("Проверка нотификации успешного входа")
    def check_success_login_message(self):
        expect(self.success_message).to_be_visible()
        expect(self.success_message).to_have_text("Вход выполнен успешно!")

    @allure.step("Проверка нотификации успешного добавления товара в корзину")
    def check_add_to_cart_success_notification(self):
        expect(self.add_to_cart_notification("success")).to_be_visible()
        expect(self.add_to_cart_notification("success")).to_have_text("Товар добавлен в корзину")

    @allure.step("Проверка нотификации неуспешного добавления товара в корзину")
    def check_add_to_cart_fail_notification(self):
        expect(self.add_to_cart_notification("warning")).to_be_visible()
        expect(self.add_to_cart_notification("warning")).to_have_text("Необходимо авторизоваться")

    @allure.step("Проверка нотификации успешного выхода из системы")
    def check_success_logout_message(self):
        expect(self.success_logout_message).to_be_visible()
        expect(self.success_logout_message).to_have_text("Вы вышли из системы")


