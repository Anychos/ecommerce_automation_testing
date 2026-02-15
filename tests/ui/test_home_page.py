from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.api.fixtures.product import CreateProductFixture

import pytest

from src.ui.pages.home import HomePage
from src.ui.pages.product_detail import ProductDetailPage
from src.ui.tools.routes import Route


@pytest.mark.ui
class TestHomePage:
    def test_check_home_page_with_products(self,
                             create_available_product: CreateProductFixture,
                             home_page: HomePage
                             ):
        home_page.open_url(Route.Home)

        home_page.check_visibility()

    @pytest.mark.parametrize(
        "click_action",
        [
            lambda card: card.click_image(),
            lambda card: card.click_title(),
            lambda card: card.click_details_link(),
        ],
        ids=["image", "title", "details"]
    )
    def test_click_product_card(
            self,
            create_available_product: CreateProductFixture,
            home_page: HomePage,
            click_action,
            product_detail_page: ProductDetailPage
    ):
        home_page.open_url(Route.Home)

        click_action(home_page.get_product_card(create_available_product.product_id))

        product_detail_page.check_url_matches(re.compile(r"/product/\d+"))

    def test_click_add_to_cart_button_unauthorized(self,
                                                   create_available_product: CreateProductFixture,
                                                   home_page: HomePage
                                                   ):
        home_page.open_url(Route.Home)

        home_page.get_product_card(create_available_product.product_id).click_add_to_cart_button()

        home_page.check_add_to_cart_fail_notification()

    def test_click_add_to_cart_button_authorized(self,
                                                 create_available_product: CreateProductFixture,
                                                 home_page_with_state: HomePage
                                                 ):
        home_page_with_state.open_url(Route.Home)

        home_page_with_state.get_product_card(create_available_product.product_id).click_add_to_cart_button()

        home_page_with_state.check_add_to_cart_success_notification()

