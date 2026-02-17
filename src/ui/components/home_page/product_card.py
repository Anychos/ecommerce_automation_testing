import re

import allure
from playwright.sync_api import Page, expect

from src.ui.components.base import BaseComponent


class ProductCard(BaseComponent):
    """
    Компонент карточки товара на главной странице
    """

    def __init__(self, page: Page, product_id: int):
        super().__init__(page)

        self.root = self.page.get_by_test_id(f"product-card-{product_id}")

        self.image = self.root.locator('[data-testid^="product-image-link-"]')
        self.stock_badge = self.root.get_by_test_id("in-stock-badge")
        self.title = self.root.locator('[data-testid^="product-name-link-"]')
        self.description = self.root.locator('[data-testid^="product-description-"]')
        self.price = self.root.locator('[data-testid^="product-price-"] span')
        self.stock_quantity = self.root.locator('[data-testid^="product-stock-"]')
        self.add_to_cart_button = self.root.locator('[data-testid^="add-to-cart-button-"]')
        self.details_link = self.root.locator('[data-testid^="product-details-link-"]')

    @allure.step("Проверка видимости элементов карточки товара")
    def check_visibility(self) -> None:
        """
        Проверяет видимость элементов карточки товара
        """

        expect(self.image).to_be_visible()
        expect(self.stock_badge).to_be_visible()
        expect(self.stock_badge).to_have_text("В наличии")

        expect(self.title).to_be_visible()
        expect(self.description).to_be_visible()

        expect(self.price).to_be_visible()
        expect(self.price).to_contain_text(re.compile(r"\d+\.\d+\s₽"))
        expect(self.stock_quantity).to_be_visible()
        expect(self.stock_quantity).to_contain_text(re.compile(r"Остаток:\s\d+\sшт\."))
        expect(self.add_to_cart_button).to_be_visible()
        expect(self.add_to_cart_button).to_have_text("В корзину")

        expect(self.details_link).to_be_visible()
        expect(self.details_link).to_have_text("Подробнее")

    @allure.step("Клик по изображению товара")
    def click_image(self) -> None:
        """
        Кликает по изображению товара
        """

        self.image.click()

    @allure.step("Клик по названию товара")
    def click_title(self) -> None:
        """
        Кликает по названию товара
        """

        self.title.click()

    @allure.step("Клик по кнопке подробнее")
    def click_details_link(self) -> None:
        """
        Кликает по кнопке подробнее
        """

        self.details_link.click()

    @allure.step("Клик по кнопке добавления товара в корзину")
    def click_add_to_cart_button(self) -> None:
        """
        Кликает по кнопке добавления товара в корзину
        """

        self.add_to_cart_button.click()
