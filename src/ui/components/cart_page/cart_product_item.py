import allure
from playwright.sync_api import Page, expect

from src.ui.components.base import BaseComponent


class CartProductItem(BaseComponent):
    """
    Компонент единицы продукта в корзине
    """

    def __init__(self, page: Page):
        super().__init__(page)

        self.root = self.page.locator("div.list-group-item")

        self.image_preview = self.root.locator("[data-testid^=cart-item-image-link-]")
        self.title = self.root.locator('[data-testid^="cart-item-name-link-"]')
        self.unit_price = self.root.locator('[data-testid^="cart-item-price-"]')
        self.quantity_input = self.root.locator("input.quantity-input")
        self.up_button = self.root.locator("button.increase-quantity")
        self.down_button = self.root.locator("button.decrease-quantity")
        self.total_price = self.root.locator('[data-testid^="item-total-price-"]')
        self.remove_button = self.root.locator("button.remove-item")

    @allure.step("Проверка видимости элементов корзины")
    def check_visibility(self) -> None:
        """
        Проверяет видимость всех элементов страницы корзины
        """

        expect(self.image_preview).to_be_visible()
        expect(self.title).to_be_visible()
        expect(self.unit_price).to_be_visible()
        expect(self.quantity_input).to_be_visible()
        expect(self.up_button).to_be_visible()
        expect(self.down_button).to_be_visible()
        expect(self.total_price).to_be_visible()
        expect(self.remove_button).to_be_visible()

    @allure.step("Клик на изображение товара")
    def click_image_preview(self) -> None:
        """
        Кликает по изображению товара
        """

        expect(self.image_preview).to_be_visible()
        self.image_preview.click()

    @allure.step("Клик на название товара")
    def click_title(self) -> None:
        """
        Кликает по названию товара
        """

        expect(self.title).to_be_visible()
        self.title.click()

    @allure.step("Изменение количества товара")
    def fill_quantity(self, quantity: int) -> None:
        """
        Изменяет количество товара в инпуте
        :param quantity: Количество товара
        """

        expect(self.quantity_input).to_be_editable()
        self.quantity_input.clear()
        self.quantity_input.fill(str(quantity))
        self.quantity_input.press("Enter")
        expect(self.quantity_input).to_have_value(str(quantity))

    @allure.step("Клик на кнопку удаления товара")
    def click_remove_button(self) -> None:
        """
        Кликает по кнопке удаления товара
        """

        expect(self.remove_button).to_be_enabled()
        self.remove_button.click()

    @allure.step("Клик на кнопку увеличения количества товара")
    def click_up_button(self) -> None:
        """
        Кликает на кнопку увеличения количества товара
        """

        expect(self.up_button).to_be_enabled()
        self.up_button.click()

    @allure.step("Клик на кнопку уменьшения количества товара")
    def click_down_button(self) -> None:
        """
        Кликает на кнопку уменьшения количества товара
        """

        expect(self.down_button).to_be_enabled()
        self.down_button.click()
