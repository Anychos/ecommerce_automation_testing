import pytest

from src.ui.pages.home import HomePage
from src.ui.pages.login import LoginPage
from src.ui.tools.routes import Route


@pytest.mark.ui
@pytest.mark.login
@pytest.mark.regression
class TestLogin:
    def test_login_page_view(self, login_page: LoginPage):
        login_page.open_url(Route.Login)

        login_page.login_form.check_visibility()

    @pytest.mark.smoke
    def test_login_success(self,
                           user,
                           login_page: LoginPage,
                           home_page: HomePage
                           ):
        login_page.open_url(Route.Login)

        login_page.login_form.fill(
            email=user.email,
            password=user.password
        )
        login_page.login_form.check_filled(
            email=user.email,
            password=user.password
        )
        login_page.login_form.click_login_button()

        home_page.check_success_login_message()
