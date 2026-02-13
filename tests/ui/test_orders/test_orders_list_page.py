import pytest

from src.ui.pages.orders import OrdersPage
from src.ui.tools.routes import Route


@pytest.mark.ui
class TestOrdersList:
    def test_check_empty_orders_list_page(self, empty_order_list_page: OrdersPage):
        empty_order_list_page.open_url(Route.OrdersList)

        empty_order_list_page.check_visibility(is_empty=True)

    def test_check_orders_list_page_with_order(self, order_list_page_with_order: OrdersPage):
        order_list_page_with_order.open_url(Route.OrdersList)

        order_list_page_with_order.check_visibility(is_empty=False)
