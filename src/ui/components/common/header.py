import allure
from playwright.sync_api import Page, expect, Locator

from src.ui.components.base import BaseComponent


class Header(BaseComponent):
    """
    Компонент хедера
    """
    def __init__(self, page: Page):
        super().__init__(page)

        self.shop_logo = self.page.get_by_test_id("navbar-brand")
        self.user_profile_dropdown_button = self.page.get_by_test_id("user-dropdown-toggle")
        self.user_profile_dropdown_menu = self.page.get_by_test_id("user-dropdown-menu")

    def nav_link(self, link_name: str) -> Locator:
        return self.page.get_by_test_id(f"nav-{link_name}-link")

    def dropdown_menu_link(self, link_name: str) -> Locator:
        return self.user_profile_dropdown_menu.get_by_test_id(f"dropdown-{link_name}-item")

    @allure.step("Проверка видимости элементов хедера")
    def check_visibility(self, *, is_logged_in: bool = False):
        expect(self.shop_logo).to_be_visible()
        expect(self.nav_link("home")).to_be_visible()
        expect(self.nav_link("home")).to_have_text("Главная")

        if is_logged_in:
            expect(self.nav_link("cart")).to_be_visible()
            expect(self.nav_link("cart")).to_have_text("Корзина")
            expect(self.nav_link("orders")).to_be_visible()
            expect(self.nav_link("orders")).to_have_text("Заказы")
            expect(self.user_profile_dropdown_button).to_be_visible()
        else:
            expect(self.nav_link("login")).to_be_visible()
            expect(self.nav_link("login")).to_have_text("Войти")
            expect(self.nav_link("register")).to_be_visible()
            expect(self.nav_link("register")).to_have_text("Регистрация")

    @allure.step("Клик по логотипу магазина")
    def click_shop_logo(self):
        self.shop_logo.click()

    @allure.step("Клик по ссылке в хедере")
    def click_nav_link(self, link_name: str):
        self.nav_link(link_name).click()

    @allure.step("Открытие дропдаун меню профиля пользователя")
    def click_user_profile_dropdown_button(self):
        self.user_profile_dropdown_button.click()
        expect(self.user_profile_dropdown_menu).to_be_visible()

    @allure.step("Клик по ссылке в дропдаун меню профиля пользователя")
    def click_dropdown_menu_link(self, link_name: str):
        expect(self.dropdown_menu_link(link_name)).to_be_visible()
        self.dropdown_menu_link(link_name).click()

