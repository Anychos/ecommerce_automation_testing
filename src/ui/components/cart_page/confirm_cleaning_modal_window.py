from playwright.sync_api import Page, expect

from src.ui.components.base import BaseComponent


class ConfirmCleaningModalWindow(BaseComponent):
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

    def check_visibility(self):
        expect(self.title).to_be_visible()
        expect(self.close_button).to_be_visible()
        expect(self.message).to_be_visible()
        expect(self.summary_title).to_be_visible()
        expect(self.removing_products_list).to_be_visible()
        expect(self.cancel_button).to_be_visible()
        expect(self.confirm_button).to_be_visible()

    def click_close_button(self):
        self.close_button.click()
        expect(self.root).not_to_be_visible()

    def click_cancel_button(self):
        self.cancel_button.click()
        expect(self.root).not_to_be_visible()

    def click_confirm_button(self):
        self.confirm_button.click()

