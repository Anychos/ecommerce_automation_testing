import allure
import pytest

from src.ui.pages.order_detail import OrderDetailPage
from utils.allure.epic import Epic
from utils.allure.severity import Severity
from utils.allure.feature import Feature
from utils.allure.story import Story


@pytest.mark.ui
@pytest.mark.order_detail
@pytest.mark.regression
@allure.epic(Epic.STORE_FRONT)
@allure.feature(Feature.USER_ORDERS)
class TestDetailOrderPage:
    @allure.story(Story.PAGE_VISIBILITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Отображение страницы детального заказа")
    def test_check_detail_order_page(self, order_detail_page: OrderDetailPage):

        order_detail_page.check_visibility()
