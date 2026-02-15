import allure
import pytest

from src.ui.pages.orders import OrdersListPage
from utils.allure.epic import Epic
from utils.allure.severity import Severity
from utils.allure.feature import Feature
from utils.allure.story import Story
from src.ui.tools.routes import Route


@pytest.mark.ui
@pytest.mark.orders_list
@pytest.mark.regression
@allure.epic(Epic.STORE_FRONT)
@allure.feature(Feature.USER_ORDERS)
class TestOrdersList:
    @allure.story(Story.PAGE_VISIBILITY)
    @allure.severity(Severity.MAJOR)
    @allure.title("Отображение пустого списка заказов")
    def test_check_empty_orders_list_page(self, empty_order_list_page: OrdersListPage):
        empty_order_list_page.open_url(Route.OrdersList)

        empty_order_list_page.check_visibility(is_empty=True)

    @allure.story(Story.PAGE_VISIBILITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Отображение списка заказов с заказом")
    def test_check_orders_list_page_with_order(self, order_list_page_with_order: OrdersListPage):
        order_list_page_with_order.open_url(Route.OrdersList)

        order_list_page_with_order.check_visibility(is_empty=False)
