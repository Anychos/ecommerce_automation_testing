from playwright.sync_api import Page, expect, Locator

from src.ui.components.base import BaseComponent


class RegistrationForm(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        self.title = self.page.get_by_test_id("register-title")
        self.registration_button = self.page.get_by_test_id("register-submit-button")
        self.already_registered_text = self.page.get_by_test_id("login-prompt-text")
        self.login_link = self.already_registered_text.get_by_role("link")

    def field_name(self, label: str) -> Locator:
        return self.page.get_by_test_id(f"{label}-label")

    def input(self, input_id: str) -> Locator:
        return self.page.locator(f"input#{input_id}")

    def check_visibility(self):
        expect(self.title).to_be_visible()
        expect(self.title).to_have_text("Регистрация")

        expect(self.field_name("email")).to_be_visible()
        expect(self.field_name("email")).to_have_text("Email")
        expect(self.input("email")).to_be_visible()

        expect(self.field_name("name")).to_be_visible()
        expect(self.field_name("name")).to_have_text("Имя")
        expect(self.input("name")).to_be_visible()

        expect(self.field_name("phone")).to_be_visible()
        expect(self.field_name("phone")).to_have_text("Телефон")
        expect(self.input("phone")).to_be_visible()

        expect(self.field_name("password")).to_be_visible()
        expect(self.field_name("password")).to_have_text("Пароль")
        expect(self.input("password")).to_be_visible()

        expect(self.field_name("confirm-password")).to_be_visible()
        expect(self.field_name("confirm-password")).to_have_text("Подтверждение пароля")
        expect(self.input("confirm_password")).to_be_visible()

        expect(self.registration_button).to_be_visible()
        expect(self.registration_button).to_have_text("Зарегистрироваться")

        expect(self.already_registered_text).to_be_visible()
        expect(self.already_registered_text).to_have_text("Уже есть аккаунт? Войдите")

    def fill(self, *, email: str, name: str, phone: str, password: str, confirm_password: str):
        expect(self.input("email")).to_be_editable()
        self.input("email").fill(email)

        expect(self.input("name")).to_be_editable()
        self.input("name").fill(name)

        expect(self.input("phone")).to_be_editable()
        self.input("phone").fill(phone)

        expect(self.input("password")).to_be_editable()
        self.input("password").fill(password)

        expect(self.input("confirm_password")).to_be_editable()
        self.input("confirm_password").fill(confirm_password)

    def check_filled(self, *, email: str, name: str, phone: str, password: str, confirm_password: str):
        expect(self.input("email")).to_have_value(email)
        expect(self.input("name")).to_have_value(name)
        expect(self.input("phone")).to_have_value(phone)
        expect(self.input("password")).to_have_value(password)
        expect(self.input("confirm_password")).to_have_value(confirm_password)

    def click_registration_button(self):
        self.registration_button.click()

    def click_login_link(self):
        self.login_link.click()
