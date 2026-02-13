import pytest

from src.ui.pages.home import HomePage
from src.ui.pages.login import LoginPage
from src.ui.pages.product_detail import ProductDetailPage
from src.ui.tools.routes import Route


@pytest.mark.ui
class TestProductDetailPage:
    def test_check_product_detail_page_authorized(self, home_page_with_state: HomePage, product_detail_page_with_state: ProductDetailPage):
        home_page_with_state.open_url(Route.Home)

        home_page_with_state.product_card.click_image()

        product_detail_page_with_state.check_visibility(is_authorized=True)

    def test_click_add_to_cart_button_authorized(self, home_page_with_state: HomePage, product_detail_page_with_state: ProductDetailPage):
        home_page_with_state.open_url(Route.Home)

        home_page_with_state.product_card.click_image()
        product_detail_page_with_state.product_info_block.click_add_to_cart_button()

        product_detail_page_with_state.check_add_to_cart_success_message()

    def test_click_add_to_cart_button_unauthorized(self, home_page: HomePage, product_detail_page: ProductDetailPage, login_page: LoginPage):
        home_page.open_url(Route.Home)

        home_page.product_card.click_image()
        product_detail_page.product_info_block.click_login_to_add_button()

        login_page.check_current_page_url("login")

