import allure
import pytest

from src.ui.pages.cart import CartPage
from src.ui.pages.checkout import CheckoutPage
from utils.allure.epic import Epic
from utils.allure.severity import Severity
from utils.allure.feature import Feature
from utils.allure.story import Story
from src.ui.tools.routes import Route


@pytest.mark.ui
@pytest.mark.cart
@pytest.mark.regression
@allure.epic(Epic.STORE_FRONT)
@allure.feature(Feature.USER_CART)
class TestCartPage:
    @allure.story(Story.PAGE_VISIBILITY)
    @allure.severity(Severity.MAJOR)
    @allure.title("Отображение пустой корзины")
    def test_check_empty_cart(self, cart_page: CartPage):
        cart_page.open_url(Route.Cart)

        cart_page.check_visibility(is_empty=True)

    @allure.story(Story.PAGE_VISIBILITY)
    @allure.severity(Severity.MAJOR)
    @allure.title("Отображение корзины с товаром")
    def test_check_cart_with_item(self, cart_page_with_product: CartPage):
        cart_page_with_product.open_url(Route.Cart)

        cart_page_with_product.check_visibility()

    @allure.story(Story.USER_CLEAR_CART)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Полная очистка корзины")
    def test_clear_cart(self, cart_page_with_product: CartPage):
        cart_page_with_product.open_url(Route.Cart)

        cart_page_with_product.click_clear_cart_button()
        cart_page_with_product.confirm_cleaning_cart_modal.check_visibility()
        cart_page_with_product.confirm_cleaning_cart_modal.click_confirm_button()

        cart_page_with_product.check_success_cleaning_notification()
        cart_page_with_product.check_visibility(is_empty=True)

    @allure.story(Story.USER_REMOVE_PRODUCT_FROM_CART)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Удаление товара из корзины")
    def test_remove_product(self, cart_page_with_product: CartPage):
        cart_page_with_product.open_url(Route.Cart)

        cart_page_with_product.product_item.click_remove_button()
        cart_page_with_product.check_success_removing_notification()

    @pytest.mark.smoke
    @allure.story(Story.USER_CREATE_ORDER)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Переход на страницу оформления заказа")
    def test_click_checkout(self, cart_page_with_product: CartPage, checkout_page: CheckoutPage):
        cart_page_with_product.open_url(Route.Cart)

        cart_page_with_product.summary_info.click_button("checkout")
        checkout_page.check_url_exact(Route.Checkout)

