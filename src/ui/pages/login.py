from playwright.sync_api import Page

from src.ui.components.common.footer import Footer
from src.ui.components.common.header import Header
from src.ui.components.login_page.login_form import LoginForm
from src.ui.pages.base import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.header = Header(self.page)
        self.login_form = LoginForm(self.page)
        self.footer = Footer(self.page)
