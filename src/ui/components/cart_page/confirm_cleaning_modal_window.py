import allure
from playwright.sync_api import Page, expect

from src.ui.components.base import BaseComponent


class ConfirmCleaningModalWindow(BaseComponent):
    """
    Компонент модального окна подтверждения очистки корзины
    """

    def __init__(self, page: Page):
        super().__init__(page)

        self.root = self.page.get_by_test_id("clear-cart-modal-content")
        self.close_button = self.root.get_by_test_id("clear-cart-modal-close")
        self.title = self.root.get_by_test_id("clear-cart-modal-title")
        self.message = self.root.get_by_test_id("warning-message")
        self.summary_title = self.root.get_by_test_id("summary-title")
        self.removing_products_list = self.root.get_by_test_id("items-list")
        self.cancel_button = self.root.get_by_test_id("cancel-clear-button")
        self.confirm_button = self.root.get_by_test_id("confirm-clear-button")

    @allure.step("Проверка видимости элементов модального окна")
    def check_visibility(self) -> None:
        """
        Проверяет видимость всех элементов модального окна
        """

        expect(self.title).to_be_visible()
        expect(self.close_button).to_be_visible()
        expect(self.message).to_be_visible()
        expect(self.summary_title).to_be_visible()
        expect(self.removing_products_list).to_be_visible()
        expect(self.cancel_button).to_be_visible()
        expect(self.confirm_button).to_be_visible()

    @allure.step("Клик на кнопку закрытия модального окна")
    def click_close_button(self) -> None:
        """
        Кликает по кнопке закрытия модального окна
        """

        expect(self.close_button).to_be_enabled()
        self.close_button.click()
        expect(self.root).not_to_be_visible()

    @allure.step("Клик на кнопку отмены очистки корзины")
    def click_cancel_button(self) -> None:
        """
        Кликает по кнопке отмены очистки корзины
        """

        self.cancel_button.click()
        expect(self.root).not_to_be_visible()

    @allure.step("Клик на кнопку подтверждения очистки корзины")
    def click_confirm_button(self) -> None:
        """
        Кликает по кнопке подтверждения очистки корзины
        """

        self.confirm_button.click()

