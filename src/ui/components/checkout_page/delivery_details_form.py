import allure
from playwright.sync_api import Page, expect, Locator

from src.ui.components.base import BaseComponent


class DeliveryDetailsForm(BaseComponent):
    """
    Компонент формы ввода данных для доставки
    """

    def __init__(self, page: Page):
        super().__init__(page)

        self.comment_input = self.page.get_by_test_id("comment-textarea")
        self.terms_checkbox = self.page.get_by_test_id("terms-checkbox")

    def title(self, test_id: str) -> Locator:
        return self.page.get_by_test_id(f"{test_id}-title")

    def field_label(self, test_id: str) -> Locator:
        return self.page.get_by_test_id(f"{test_id}-label")

    def field_input(self, test_id: str) -> Locator:
        return self.page.get_by_test_id(f"{test_id}-input")

    def description(self, test_id: str) -> Locator:
        return self.page.get_by_test_id(f"{test_id}-description")

    def error_message(self, test_id: str) -> Locator:
        return self.page.get_by_test_id(f"{test_id}-error")

    def radio_button(self, test_id: str) -> Locator:
        return self.page.get_by_test_id(f"{test_id}-radio")

    @allure.step("Проверка видимости элементов формы доставки")
    def check_visibility(self) -> None:
        """
        Проверяет видимость элементов формы доставки
        """

        expect(self.title("form")).to_be_visible()
        expect(self.title("form")).to_have_text("Данные для доставки")

        expect(self.title("user-info")).to_be_visible()
        expect(self.title("user-info")).to_have_text("Ваши данные")

        expect(self.field_label("name")).to_be_visible()
        expect(self.field_label("name")).to_have_text("ФИО *")
        expect(self.field_input("name")).to_be_visible()

        expect(self.field_label("phone")).to_be_visible()
        expect(self.field_label("phone")).to_have_text("Телефон *")
        expect(self.field_input("phone")).to_be_visible()

        expect(self.field_label("email")).to_be_visible()
        expect(self.field_label("email")).to_have_text("Email *")
        expect(self.field_input("email")).to_be_visible()

        expect(self.title("delivery")).to_be_visible()
        expect(self.title("delivery")).to_have_text("Адрес доставки")

        expect(self.field_label("address")).to_be_visible()
        expect(self.field_label("address")).to_have_text("Адрес *")
        expect(self.field_input("address")).to_be_visible()

        expect(self.field_label("zip")).to_be_visible()
        expect(self.field_label("zip")).to_have_text("Индекс")
        expect(self.field_input("zip")).to_be_visible()

        expect(self.field_label("comment")).to_be_visible()
        expect(self.field_label("comment")).to_have_text("Комментарий к доставке")
        expect(self.comment_input).to_be_visible()

        expect(self.title("payment")).to_be_visible()
        expect(self.title("payment")).to_have_text("Способ оплаты")

        expect(self.title("card-payment")).to_be_visible()
        expect(self.title("card-payment")).to_have_text("Банковская карта")
        expect(self.radio_button("card-payment")).to_be_visible()
        expect(self.description("card-payment")).to_be_visible()

        expect(self.title("cash-payment")).to_be_visible()
        expect(self.title("cash-payment")).to_have_text("Наличные при получении")
        expect(self.radio_button("cash-payment")).to_be_visible()
        expect(self.description("cash-payment")).to_be_visible()

        expect(self.terms_checkbox).to_be_visible()
        expect(self.terms_checkbox).not_to_be_checked()
        expect(self.field_label("terms")).to_be_visible()
        expect(self.field_label("terms")).to_have_text("Я соглашаюсь с условиями обработки персональных данных и политикой конфиденциальности *")

    @allure.step("Заполнение формы")
    def fill(self,
             *,
             name: str,
             phone: str,
             email: str,
             address: str,
             zip: str = "",
             comment: str = "",
             is_full_data: bool = False
             ) -> None:
        """
        Заполняет форму доставки

        :param name: Имя пользователя
        :param phone: Телефон пользователя
        :param email: Email пользователя
        :param address: Адрес пользователя
        :param zip: Почтовый индекс пользователя
        :param comment: Комментарий к доставке
        :param is_full_data: Флаг заполнения всех данных
        """

        expect(self.field_input("name")).to_be_editable()
        self.field_input("name").fill(name)

        expect(self.field_input("phone")).to_be_editable()
        self.field_input("phone").fill(phone)

        expect(self.field_input("email")).to_be_editable()
        self.field_input("email").fill(email)

        expect(self.field_input("address")).to_be_editable()
        self.field_input("address").fill(address)

        if is_full_data:
            expect(self.field_input("zip")).to_be_editable()
            self.field_input("zip").fill(zip)

            expect(self.comment_input).to_be_editable()
            self.comment_input.fill(comment)

    @allure.step("Проверка заполнения формы")
    def check_filled(self,
                     *,
                     name: str,
                     phone: str,
                     email: str,
                     address: str,
                     zip: str = "",
                     comment: str = "",
                     is_full_data: bool = False
                     ) -> None:
        """
        Проверяет заполнение формы доставки

        :param name: Имя пользователя
        :param phone: Телефон пользователя
        :param email: Email пользователя
        :param address: Адрес пользователя
        :param zip: Почтовый индекс пользователя
        :param comment: Комментарий к доставке
        :param is_full_data: Флаг заполнения всех данных
        """

        if is_full_data:
            expect(self.field_input("name")).to_have_value(name)
            expect(self.field_input("phone")).to_have_value(phone)
            expect(self.field_input("email")).to_have_value(email)
            expect(self.field_input("address")).to_have_value(address)
        else:
            expect(self.field_input("zip")).to_have_value(zip)
            expect(self.comment_input).to_have_value(comment)

    @allure.step("Выбор способа оплаты")
    def select_payment_method(self, payment_method: str) -> None:
        """
        Выбирает способ оплаты
        :param payment_method: Способ оплаты
        """

        expect(self.radio_button(payment_method)).to_be_visible()
        self.radio_button(payment_method).click()
        expect(self.radio_button(payment_method)).to_be_checked()

    @allure.step("Клик по чекбоксу согласия на обработку персональных данных")
    def click_terms_checkbox(self) -> None:
        """
        Кликает по чекбоксу согласия на обработку персональных данных
        """

        expect(self.terms_checkbox).to_be_visible()
        self.terms_checkbox.click()
        expect(self.terms_checkbox).to_be_checked()
