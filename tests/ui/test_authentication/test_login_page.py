import allure
import pytest

from src.ui.pages.home import HomePage
from src.ui.pages.login import LoginPage
from src.ui.tools.routes import Route
from utils.allure.epic import Epic
from utils.allure.severity import Severity
from utils.allure.feature import Feature
from utils.allure.story import Story


@pytest.mark.ui
@pytest.mark.login
@pytest.mark.regression
@allure.epic(Epic.STORE_FRONT)
@allure.feature(Feature.AUTHENTICATION)
class TestLogin:
    @allure.story(Story.PAGE_VISIBILITY)
    @allure.severity(Severity.MAJOR)
    @allure.title("Отображение страницы логина")
    def test_login_page_view(self, login_page: LoginPage):
        login_page.open_url(Route.Login)

        login_page.login_form.check_visibility()

    @pytest.mark.smoke
    @allure.story(Story.USER_LOGIN)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Логин существующего пользователя")
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
