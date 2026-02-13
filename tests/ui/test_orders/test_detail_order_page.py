import pytest

from src.ui.pages.order_detail import OrderDetailPage


@pytest.mark.ui
class TestDetailOrderPage:
    def test_check_detail_order_page(self, order_detail_page: OrderDetailPage):

        order_detail_page.check_visibility()
