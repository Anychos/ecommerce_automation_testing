from __future__ import annotations

import re
from typing import TYPE_CHECKING

import allure

from utils.allure.epic import Epic
from utils.allure.severity import Severity
from utils.allure.feature import Feature
from utils.allure.story import Story

if TYPE_CHECKING:
    from src.api.fixtures.product import CreateProductFixture

import pytest

from src.ui.pages.home import HomePage
from src.ui.pages.product_detail import ProductDetailPage
from src.ui.tools.routes import Route


@pytest.mark.ui
@pytest.mark.home
@pytest.mark.regression
@allure.epic(Epic.STORE_FRONT)
class TestHomePage:
    @allure.feature(Feature.HOME_PAGE)
    @allure.story(Story.PAGE_VISIBILITY)
    @allure.severity(Severity.MAJOR)
    @allure.title("Отображение главной страницы")
    def test_check_home_page_with_products(self,
                             create_available_product: CreateProductFixture,
                             home_page: HomePage
                             ):
        home_page.open_url(Route.Home)

        home_page.check_visibility()

    @pytest.mark.smoke
    @allure.feature(Feature.USER_PRODUCTS)
    @allure.story(Story.USER_GET_PRODUCT_BY_ID)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Открытие карточки товара")
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

    @allure.feature(Feature.USER_CART)
    @allure.story(Story.USER_ADD_ITEM_TO_CART)
    @allure.severity(Severity.MAJOR)
    @allure.title("Добавление товара в корзину без авторизации")
    def test_click_add_to_cart_button_unauthorized(self,
                                                   create_available_product: CreateProductFixture,
                                                   home_page: HomePage
                                                   ):
        home_page.open_url(Route.Home)

        home_page.get_product_card(create_available_product.product_id).click_add_to_cart_button()

        home_page.check_add_to_cart_fail_notification()

    @pytest.mark.smoke
    @allure.feature(Feature.USER_CART)
    @allure.story(Story.USER_ADD_ITEM_TO_CART)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Добавление товара в корзину с авторизацией")
    def test_click_add_to_cart_button_authorized(self,
                                                 create_available_product: CreateProductFixture,
                                                 home_page_with_state: HomePage
                                                 ):
        home_page_with_state.open_url(Route.Home)

        home_page_with_state.get_product_card(create_available_product.product_id).click_add_to_cart_button()

        home_page_with_state.check_add_to_cart_success_notification()

