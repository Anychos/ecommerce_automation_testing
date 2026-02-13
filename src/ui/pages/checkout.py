from playwright.sync_api import Page, expect

from src.ui.components.checkout_page.delivery_details_form import DeliveryDetailsForm
from src.ui.components.common.order_summary import OrderSummary
from src.ui.pages.base import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.checkout_success_notification = self.page.get_by_test_id("checkout-notification")
        self.delivery_details_form = DeliveryDetailsForm(self.page)
        self.summary_info = OrderSummary(self.page, self.page.get_by_test_id("order-summary-card"))

    def check_success_order_notification(self):
        expect(self.checkout_success_notification).to_be_visible()
        expect(self.checkout_success_notification).to_have_text("Заказ успешно создан!")
