from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.api.fixtures.product import CreateProductFixture

import pytest
from playwright.sync_api import Page

from src.ui.pages.cart import CartPage
from src.ui.pages.checkout import CheckoutPage
from src.ui.pages.home import HomePage
from src.ui.pages.login import LoginPage
from src.ui.pages.order_detail import OrderDetailPage
from src.ui.pages.orders import OrdersPage
from src.ui.pages.product_detail import ProductDetailPage
from src.ui.pages.registration import RegistrationPage
from src.ui.tools.data_generator import fake_ru
from src.ui.tools.routes import Route


@pytest.fixture
def registration_page(chromium_page: Page) -> RegistrationPage:
    return RegistrationPage(chromium_page)


@pytest.fixture
def login_page(chromium_page: Page) -> LoginPage:
    return LoginPage(chromium_page)


@pytest.fixture
def home_page(chromium_page: Page) -> HomePage:
    return HomePage(chromium_page)


@pytest.fixture
def home_page_with_state(function_chromium_page_with_state: Page) -> HomePage:
    return HomePage(function_chromium_page_with_state)


@pytest.fixture
def cart_page(function_chromium_page_with_state: Page) -> CartPage:
    return CartPage(function_chromium_page_with_state)


@pytest.fixture
def cart_page_with_product(create_available_product: CreateProductFixture, home_page_with_state: HomePage, cart_page: CartPage) -> CartPage:
    home_page_with_state.open_url(Route.Home)

    home_page_with_state.get_product_card(create_available_product.product_id).click_add_to_cart_button()
    home_page_with_state.check_add_to_cart_success_notification()

    return cart_page


@pytest.fixture
def product_detail_page(chromium_page: Page) -> ProductDetailPage:
    return ProductDetailPage(chromium_page)


@pytest.fixture
def product_detail_page_with_state(function_chromium_page_with_state: Page) -> ProductDetailPage:
    return ProductDetailPage(function_chromium_page_with_state)


@pytest.fixture
def checkout_page(cart_page_with_product: CartPage) -> CheckoutPage:
    return CheckoutPage(cart_page_with_product.page)


@pytest.fixture
def order_list_page(function_chromium_page_with_state: Page) -> OrdersPage:
    return OrdersPage(function_chromium_page_with_state)


@pytest.fixture
def empty_order_list_page(function_chromium_page_with_state: Page) -> OrdersPage:
    return OrdersPage(function_chromium_page_with_state)


@pytest.fixture
def order_detail_page(order_list_page_with_order: OrdersPage) -> OrderDetailPage:
    return OrderDetailPage(order_list_page_with_order.page)


@pytest.fixture
def order_list_page_with_order(checkout_page: CheckoutPage, order_list_page: OrdersPage) -> OrdersPage:
    checkout_page.open_url(Route.Checkout)

    checkout_page.delivery_details_form.fill(
        name=fake_ru.full_name(),
        phone=fake_ru.phone_number(),
        email=fake_ru.email(),
        address=fake_ru.address()
    )
    checkout_page.delivery_details_form.click_terms_checkbox()
    checkout_page.summary_info.click_button("place-order")
    checkout_page.check_success_order_notification()
    order_list_page.check_url_matches(re.compile(r"/orders/\d+"))

    return order_list_page


