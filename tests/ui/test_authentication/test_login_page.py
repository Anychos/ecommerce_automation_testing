import pytest

from config import settings
from src.ui.pages.home import HomePage
from src.ui.pages.login import LoginPage
from src.ui.tools.routes import Route


@pytest.mark.ui
class TestLogin:
    def test_login_page_view(self, login_page: LoginPage):
        login_page.open_url(Route.Login)

        login_page.login_form.check_visibility()

    def test_login_success(self,
                           login_page: LoginPage,
                           home_page: HomePage
                           ):
        login_page.open_url(Route.Login)

        login_page.login_form.fill(
            email=settings.test_user_login.email,
            password=settings.test_user_login.password
        )
        login_page.login_form.check_filled(
            email=settings.test_user_login.email,
            password=settings.test_user_login.password
        )
        login_page.login_form.click_login_button()

        home_page.check_success_login_message()
