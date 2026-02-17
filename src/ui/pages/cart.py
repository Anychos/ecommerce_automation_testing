import allure
from playwright.sync_api import Page, expect

from src.ui.components.cart_page.cart_product_item import CartProductItem
from src.ui.components.cart_page.confirm_cleaning_modal_window import ConfirmCleaningModalWindow
from src.ui.components.common.empty_view import EmptyView
from src.ui.components.common.footer import Footer
from src.ui.components.common.header import Header
from src.ui.components.common.order_summary import OrderSummary
from src.ui.pages.base import BasePage


class CartPage(BasePage):
    """
    Класс страницы корзины
    """

    def __init__(self, page: Page):
        super().__init__(page)

        self.header = Header(self.page)

        self.confirm_cleaning_cart_modal = ConfirmCleaningModalWindow(self.page)
        self.remove_product_success_message = self.page.get_by_test_id("cart-notification")

        self.page_title = self.page.get_by_test_id("cart-title")

        self.empty_view = EmptyView(self.page, "cart")
        self.go_to_products_button = self.page.get_by_test_id("browse-products-button")

        self.items_container = self.page.get_by_test_id("cart-items-card")
        self.cart_title = self.items_container.get_by_test_id("cart-number")
        self.items_count_text = self.items_container.get_by_test_id("items-count")
        self.clear_cart_button = self.items_container.get_by_test_id("clear-cart-button")

        self.product_item = CartProductItem(self.page)

        self.summary_info = OrderSummary(self.page, self.page.get_by_test_id("cart-summary-card"))

        self.footer = Footer(self.page)

    @allure.step("Проверка видимости элементов страницы корзины")
    def check_visibility(self,
                         *,
                         is_empty: bool = False,
                         is_free_delivery: bool = False
                         ) -> None:
        """
        Проверяет видимость элементов страницы корзины

        :param is_empty: Флаг пустой корзины
        :param is_free_delivery: Флаг бесплатной доставки
        """

        expect(self.page_title).to_be_visible()
        if is_empty:
            self.empty_view.check_visibility()
            expect(self.go_to_products_button).to_be_visible()
            expect(self.go_to_products_button).to_have_text("Перейти к товарам")
        else:
            expect(self.cart_title).to_be_visible()
            expect(self.items_count_text).to_be_visible()
            expect(self.clear_cart_button).to_be_visible()
            self.product_item.check_visibility()
            self.summary_info.check_visibility(page_name="cart", is_free_delivery=is_free_delivery)

    @allure.step("Клик по кнопке перейти к товарам")
    def click_go_to_products_button(self) -> None:
        """
        Кликает по кнопке перейти к товарам
        """

        expect(self.go_to_products_button).to_be_enabled()
        self.go_to_products_button.click()

    @allure.step("Клик по кнопке очистить корзину")
    def click_clear_cart_button(self) -> None:
        """
        Кликает по кнопке очистить корзину
        """

        expect(self.clear_cart_button).to_be_enabled()
        self.clear_cart_button.click()

    @allure.step("Проверка нотификации успешного удаления товара из корзины")
    def check_success_removing_notification(self) -> None:
        """
        Проверяет нотификацию успешного удаления товара из корзины
        """

        expect(self.remove_product_success_message).to_be_visible()
        expect(self.remove_product_success_message).to_have_text("Товар удален из корзины")

    @allure.step("Проверка нотификации успешной очистки корзины")
    def check_success_cleaning_notification(self) -> None:
        """
        Проверяет нотификацию успешной очистки корзины
        """

        expect(self.remove_product_success_message).to_be_visible()
        expect(self.remove_product_success_message).to_have_text("Корзина очищена")


