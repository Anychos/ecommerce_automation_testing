import pytest

from src.ui.pages.orders import OrdersListPage
from src.ui.tools.routes import Route


@pytest.mark.ui
@pytest.mark.orders_list
@pytest.mark.regression
class TestOrdersList:
    def test_check_empty_orders_list_page(self, empty_order_list_page: OrdersListPage):
        empty_order_list_page.open_url(Route.OrdersList)

        empty_order_list_page.check_visibility(is_empty=True)

    def test_check_orders_list_page_with_order(self, order_list_page_with_order: OrdersListPage):
        order_list_page_with_order.open_url(Route.OrdersList)

        order_list_page_with_order.check_visibility(is_empty=False)
