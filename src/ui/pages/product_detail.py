from playwright.sync_api import Page, expect

from src.ui.components.common.footer import Footer
from src.ui.components.common.header import Header
from src.ui.components.product_detail_page.product_info_block import ProductInfoBlock
from src.ui.pages.base import BasePage


class ProductDetailPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.header = Header(self.page)

        self.navigation_chain = self.page.get_by_test_id("breadcrumb-list")
        self.navigation_chain_home_link = self.navigation_chain.get_by_test_id("breadcrumb-home-link")
        self.navigation_chain_current = self.navigation_chain.get_by_test_id("breadcrumb-current")
        self.product_info_block = ProductInfoBlock(self.page)
        self.add_to_cart_success_message = self.page.get_by_test_id("action-notification")

        self.footer = Footer(self.page)

    def check_visibility(self, *, is_authorized: bool = False):
        expect(self.navigation_chain).to_be_visible()
        expect(self.navigation_chain_home_link).to_be_visible()
        expect(self.navigation_chain_current).to_be_visible()
        self.product_info_block.check_visibility(is_authorized=is_authorized)

    def click_home_link(self):
        self.navigation_chain_home_link.click()

    def check_add_to_cart_success_message(self):
        expect(self.add_to_cart_success_message).to_be_visible()
        expect(self.add_to_cart_success_message).to_have_text("Товар добавлен в корзину")


