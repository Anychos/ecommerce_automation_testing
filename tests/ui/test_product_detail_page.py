from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.api.fixtures.product import CreateProductFixture

import pytest

from src.ui.pages.home import HomePage
from src.ui.pages.login import LoginPage
from src.ui.pages.product_detail import ProductDetailPage
from src.ui.tools.routes import Route


@pytest.mark.ui
@pytest.mark.product_detail
@pytest.mark.regression
class TestProductDetailPage:
    def test_check_product_detail_page_authorized(self,
                                                  create_available_product: CreateProductFixture,
                                                  home_page_with_state: HomePage,
                                                  product_detail_page_with_state: ProductDetailPage
                                                  ):
        home_page_with_state.open_url(Route.Home)

        home_page_with_state.get_product_card(create_available_product.product_id).click_image()

        product_detail_page_with_state.check_visibility(is_authorized=True)

    @pytest.mark.smoke
    def test_click_add_to_cart_button_authorized(self,
                                                 create_available_product: CreateProductFixture,
                                                 home_page_with_state: HomePage,
                                                 product_detail_page_with_state: ProductDetailPage
                                                 ):
        home_page_with_state.open_url(Route.Home)

        home_page_with_state.get_product_card(create_available_product.product_id).click_image()
        product_detail_page_with_state.product_info_block.click_add_to_cart_button()

        product_detail_page_with_state.check_add_to_cart_success_message()

    def test_click_add_to_cart_button_unauthorized(self,
                                                   create_available_product: CreateProductFixture,
                                                   home_page: HomePage,
                                                   product_detail_page: ProductDetailPage,
                                                   login_page: LoginPage
                                                   ):
        home_page.open_url(Route.Home)

        home_page.get_product_card(create_available_product.product_id).click_image()
        product_detail_page.product_info_block.click_login_to_add_button()

        login_page.check_url_exact(Route.Login)

