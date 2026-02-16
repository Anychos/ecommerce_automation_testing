import re

import allure
import pytest

from src.ui.pages.checkout import CheckoutPage
from src.ui.tools.data_generator import fake_ru
from src.ui.tools.routes import Route
from utils.allure.epic import Epic
from utils.allure.feature import Feature
from utils.allure.severity import Severity
from utils.allure.story import Story


@pytest.mark.ui
@pytest.mark.checkout
@pytest.mark.regression
@allure.epic(Epic.STORE_FRONT)
@allure.feature(Feature.USER_ORDERS)
class TestCheckoutPage:
    @allure.story(Story.PAGE_VISIBILITY)
    @allure.severity(Severity.MAJOR)
    @allure.title("Отображение страницы оформления заказа")
    def test_check_checkout_page(self, checkout_page: CheckoutPage):
        checkout_page.open_url(Route.Checkout)

        checkout_page.delivery_details_form.check_visibility()
        checkout_page.summary_info.check_visibility(page_name="checkout")

    @pytest.mark.smoke
    @allure.story(Story.USER_CREATE_ORDER)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Оформление заказа")
    def test_make_order_required_data(self, checkout_page: CheckoutPage):
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
        checkout_page.check_url_matches(re.compile(r"/orders/\d+"))
