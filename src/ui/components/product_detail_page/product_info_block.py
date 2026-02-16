import re

import allure
from playwright.sync_api import Page, expect

from src.ui.components.base import BaseComponent


class ProductInfoBlock(BaseComponent):
    """
    Компонент блока информации о товаре
    """
    def __init__(self, page: Page):
        super().__init__(page)

        self.image_container = self.page.get_by_test_id("product-image-card")
        self.image = self.image_container.get_by_test_id("product-main-image")
        self.stock_badge = self.image_container.get_by_test_id("in-stock-badge")

        self.info_container = self.page.get_by_test_id("product-info-card")
        self.title = self.info_container.get_by_test_id("product-name")
        self.article_text = self.info_container.get_by_test_id("product-id-container")
        self.article_label = self.article_text.get_by_test_id("product-id-label")
        self.article_value = self.article_text.get_by_test_id("product-id-value")
        self.price = self.info_container.get_by_test_id("product-price")
        self.stock_text = self.info_container.get_by_test_id("stock-quantity-text")
        self.description_title = self.info_container.get_by_test_id("description-title")
        self.description = self.info_container.get_by_test_id("product-description")
        self.add_to_cart_button = self.info_container.get_by_test_id("add-to-cart-button")
        self.login_to_add_button = self.info_container.get_by_test_id("login-to-add-button")
        self.additional_info_section = self.info_container.get_by_test_id("additional-info-section")

    @allure.step("Проверка видимости элементов блока информации о товаре")
    def check_visibility(self, *, is_authorized: bool = False):
        expect(self.image).to_be_visible()
        expect(self.stock_badge).to_be_visible()

        expect(self.title).to_be_visible()
        expect(self.article_label).to_be_visible()
        expect(self.article_label).to_have_text("Артикул:")
        expect(self.article_value).to_be_visible()
        expect(self.price).to_be_visible()
        expect(self.price).to_contain_text(re.compile(r"\d+\.\d+\s₽"))
        expect(self.stock_text).to_be_visible()
        expect(self.stock_text).to_contain_text(re.compile(r"В наличии:\s\d+\sшт\."))
        expect(self.description_title).to_be_visible()
        expect(self.description_title).to_have_text("Описание")
        expect(self.description).to_be_visible()

        if is_authorized:
            expect(self.add_to_cart_button).to_be_visible()
            expect(self.add_to_cart_button).to_have_text("Добавить в корзину")
        else:
            expect(self.login_to_add_button).to_be_visible()
            expect(self.login_to_add_button).to_have_text("Войдите, чтобы добавить в корзину")

        expect(self.additional_info_section).to_be_visible()

    @allure.step("Клик по кнопке добавить в корзину")
    def click_add_to_cart_button(self):
        self.add_to_cart_button.click()

    @allure.step("Клик по кнопке войдите, чтобы добавить в корзину")
    def click_login_to_add_button(self):
        self.login_to_add_button.click()

