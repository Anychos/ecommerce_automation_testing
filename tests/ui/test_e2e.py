import allure
import pytest

from src.ui.pages.cart import CartPage
from src.ui.pages.checkout import CheckoutPage
from src.ui.pages.home import HomePage
from src.ui.pages.login import LoginPage
from src.ui.pages.order_detail import OrderDetailPage
from src.ui.pages.orders import OrdersListPage
from src.ui.pages.product_detail import ProductDetailPage
from src.ui.pages.registration import RegistrationPage
from utils.allure.epic import Epic
from utils.allure.severity import Severity


@pytest.mark.ui
@pytest.mark.e2e
@allure.epic(Epic.STORE_FRONT)
class TestE2E:
    @allure.severity(Severity.BLOCKER)
    @allure.title("E2E путь пользователя")
    @pytest.mark.skip
    def test_e2e_user_flow(self,
                           home_page: HomePage,
                           registration_page: RegistrationPage,
                           login_page: LoginPage,
                           product_detail_page: ProductDetailPage,
                           cart_page: CartPage,
                           checkout_page: CheckoutPage,
                           order_detail_page: OrderDetailPage,
                           order_list_page: OrdersListPage,
                           ):
        pass
