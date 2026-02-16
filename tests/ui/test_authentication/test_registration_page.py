import allure
import pytest

from src.ui.pages.home import HomePage
from src.ui.pages.registration import RegistrationPage
from src.ui.tools.routes import Route
from utils.allure.epic import Epic
from utils.allure.feature import Feature
from utils.allure.severity import Severity
from utils.allure.story import Story


@pytest.mark.ui
@pytest.mark.registration
@pytest.mark.regression
@allure.epic(Epic.STORE_FRONT)
@allure.feature(Feature.AUTHENTICATION)
class TestRegistration:
    @allure.story(Story.PAGE_VISIBILITY)
    @allure.severity(Severity.MAJOR)
    @allure.title("Отображение страницы регистрации")
    def test_registration_page_view(self, registration_page: RegistrationPage):
        registration_page.open_url(Route.Registration)

        registration_page.registration_form.check_visibility()

    @pytest.mark.smoke
    @allure.story(Story.USER_REGISTRATION)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Регистрация нового пользователя")
    def test_registration_success(self,
                                  registration_page: RegistrationPage,
                                  home_page: HomePage,
                                  user_data_function
                                  ):
        registration_page.open_url(Route.Registration)

        registration_page.registration_form.fill(
            email=user_data_function.email,
            name=user_data_function.name,
            phone=user_data_function.phone,
            password=user_data_function.password,
            confirm_password=user_data_function.password
        )
        registration_page.registration_form.check_filled(
            email=user_data_function.email,
            name=user_data_function.name,
            phone=user_data_function.phone,
            password=user_data_function.password,
            confirm_password=user_data_function.confirm_password
        )
        registration_page.registration_form.click_registration_button()

        home_page.check_success_registration_message()


