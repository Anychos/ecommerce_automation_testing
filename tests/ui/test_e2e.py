from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Page

from src.ui.tools.data_generator import fake_ru

if TYPE_CHECKING:
    from src.api.fixtures.product import CreateProductFixture

import allure
import pytest

from config import settings
from src.ui.pages.cart import CartPage
from src.ui.pages.checkout import CheckoutPage
from src.ui.pages.home import HomePage
from src.ui.pages.login import LoginPage
from src.ui.pages.order_detail import OrderDetailPage
from src.ui.pages.orders import OrdersListPage
from src.ui.pages.product_detail import ProductDetailPage
from src.ui.pages.registration import RegistrationPage
from src.ui.tools.routes import Route
from utils.allure.epic import Epic
from utils.allure.severity import Severity


@pytest.mark.ui
@pytest.mark.e2e
@allure.epic(Epic.STORE_FRONT)
class TestE2E:
    @allure.severity(Severity.BLOCKER)
    @allure.title("E2E путь пользователя")
    def test_e2e_user_flow(self,
                           chromium_page: Page,
                           create_available_product: CreateProductFixture
                           ):
        home_page = HomePage(chromium_page)
        registration_page = RegistrationPage(chromium_page)
        login_page = LoginPage(chromium_page)
        product_detail_page = ProductDetailPage(chromium_page)
        cart_page = CartPage(chromium_page)
        checkout_page = CheckoutPage(chromium_page)
        order_detail_page = OrderDetailPage(chromium_page)
        order_list_page = OrdersListPage(chromium_page)

        home_page.open_url(Route.Home)

        home_page.header.check_visibility()
        home_page.header.click_nav_link("register")

        registration_page.registration_form.check_visibility()
        registration_page.registration_form.fill(
            email=settings.test_user.email,
            name=settings.test_user.name,
            phone=settings.test_user.phone,
            password=settings.test_user.password,
            confirm_password=settings.test_user.confirm_password
        )
        registration_page.registration_form.check_filled(
            email=settings.test_user.email,
            name=settings.test_user.name,
            phone=settings.test_user.phone,
            password=settings.test_user.password,
            confirm_password=settings.test_user.confirm_password
        )
        registration_page.registration_form.click_registration_button()

        home_page.header.check_visibility(is_logged_in=True)

        home_page.header.click_user_profile_dropdown_button()
        home_page.header.click_dropdown_menu_link("logout")

        home_page.header.check_visibility()

        home_page.header.click_nav_link("login")

        login_page.login_form.check_visibility()
        login_page.login_form.fill(
            email=settings.test_user.email,
            password=settings.test_user.password
        )
        login_page.login_form.check_filled(
            email=settings.test_user.email,
            password=settings.test_user.password
        )
        login_page.login_form.click_login_button()

        home_page.header.check_visibility(is_logged_in=True)

        home_page.get_product_card(create_available_product.product_id).click_image()

        product_detail_page.product_info_block.click_add_to_cart_button()
        product_detail_page.header.click_nav_link("cart")

        cart_page.check_visibility()
        cart_page.summary_info.click_button("checkout")

        checkout_page.summary_info.check_visibility(page_name="checkout")

        checkout_page.delivery_details_form.fill(
            name=settings.test_user.name,
            phone=settings.test_user.phone,
            email=settings.test_user.email,
            address=fake_ru.address()
        )
        checkout_page.delivery_details_form.click_terms_checkbox()
        checkout_page.summary_info.click_button("place-order")

        order_detail_page.check_visibility()

        home_page.header.click_nav_link("orders")
        order_list_page.check_visibility()

