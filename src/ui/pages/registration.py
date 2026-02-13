from playwright.sync_api import Page

from src.ui.components.common.footer import Footer
from src.ui.components.common.header import Header
from src.ui.components.registration_page.registration_form import RegistrationForm
from src.ui.pages.base import BasePage


class RegistrationPage(BasePage):
    """
    Класс страницы регистрации

    Описывает ее локаторы, компоненты и методы взаимодействия
    """
    def __init__(self, page: Page):
        super().__init__(page)

        self.header = Header(self.page)
        self.registration_form = RegistrationForm(self.page)
        self.footer = Footer(self.page)
