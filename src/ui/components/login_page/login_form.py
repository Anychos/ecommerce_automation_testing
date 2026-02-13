from playwright.sync_api import Locator, Page, expect

from src.ui.components.base import BaseComponent


class LoginForm(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        self.title = self.page.get_by_test_id("login-title")
        self.remember_me_checkbox = self.page.get_by_test_id("remember-me-checkbox")
        self.remember_me_text = self.page.get_by_test_id("remember-me-label")
        self.login_button = self.page.get_by_test_id("login-submit-button")
        self.registration_text = self.page.get_by_test_id("register-prompt-text")
        self.registration_link = self.registration_text.get_by_role("link")

    def field_name(self, label: str) -> Locator:
        return self.page.get_by_test_id(f"{label}-label")

    def input(self, input_id: str) -> Locator:
        return self.page.locator(f'input#{input_id}')

    def check_visibility(self):
        expect(self.title).to_be_visible()
        expect(self.title).to_have_text("Вход в систему")

        expect(self.field_name("login-email")).to_be_visible()
        expect(self.field_name("login-email")).to_have_text("Email")
        expect(self.input("email")).to_be_visible()

        expect(self.field_name("login-password")).to_be_visible()
        expect(self.field_name("login-password")).to_have_text("Пароль")
        expect(self.input("password")).to_be_visible()

        expect(self.remember_me_checkbox).to_be_visible()
        expect(self.remember_me_checkbox).not_to_be_checked()
        expect(self.remember_me_text).to_be_visible()
        expect(self.remember_me_text).to_have_text("Запомнить меня")

        expect(self.login_button).to_be_visible()
        expect(self.login_button).to_have_text("Войти")

        expect(self.registration_text).to_be_visible()
        expect(self.registration_text).to_have_text("Нет аккаунта? Зарегистрируйтесь")

    def fill(self, *, email: str, password: str):
        expect(self.input("email")).to_be_editable()
        self.input("email").fill(email)

        expect(self.input("password")).to_be_editable()
        self.input("password").fill(password)

    def check_filled(self, *, email: str, password: str):
        expect(self.input("email")).to_have_value(email)
        expect(self.input("password")).to_have_value(password)

    def click_remember_me_checkbox(self):
        self.remember_me_checkbox.click()

    def check_remember_me_checkbox(self, *, is_checked: bool = False):
        if is_checked:
            expect(self.remember_me_checkbox).to_be_checked()
        else:
            expect(self.remember_me_checkbox).not_to_be_checked()

    def click_login_button(self):
        self.login_button.click()

    def click_registration_link(self):
        self.registration_link.click()
