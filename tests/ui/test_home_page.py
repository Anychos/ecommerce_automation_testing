import pytest

from src.ui.pages.home import HomePage
from src.ui.pages.product_detail import ProductDetailPage
from src.ui.tools.routes import Route


@pytest.mark.ui
class TestHomePage:
    def test_check_home_page(self, home_page: HomePage):
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
            home_page: HomePage,
            click_action,
            product_detail_page: ProductDetailPage
    ):
        home_page.open_url(Route.Home)

        click_action(home_page.product_card)

        product_detail_page.check_current_page_url("product")

    def test_click_add_to_cart_button_unauthorized(self, home_page: HomePage):
        home_page.open_url(Route.Home)

        home_page.product_card.click_add_to_cart_button()

        home_page.check_add_to_cart_fail_notification()

    def test_click_add_to_cart_button_authorized(self, home_page_with_state: HomePage):
        home_page_with_state.open_url(Route.Home)

        home_page_with_state.product_card.click_add_to_cart_button()

        home_page_with_state.check_add_to_cart_success_notification()

