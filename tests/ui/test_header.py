import re

import allure
import pytest

from src.ui.pages.home import HomePage
from utils.allure.epic import Epic
from utils.allure.severity import Severity
from utils.allure.feature import Feature
from utils.allure.story import Story
from src.ui.tools.routes import Route


@pytest.mark.ui
@pytest.mark.header
@pytest.mark.regression
@allure.epic(Epic.STORE_FRONT)
class TestHeader:
    @allure.story(Story.PAGE_VISIBILITY)
    @allure.severity(Severity.MAJOR)
    @allure.title("Отображение хедера в неавторизованном состоянии")
    def test_header_visibility_unauthorized(self, home_page: HomePage):
        home_page.open_url(Route.Home)

        home_page.header.check_visibility()

    @allure.story(Story.PAGE_VISIBILITY)
    @allure.severity(Severity.MAJOR)
    @allure.title("Отображение хедера в авторизованном состоянии")
    def test_header_visibility_authorized(self, home_page_with_state: HomePage):
        home_page_with_state.open_url(Route.Home)

        home_page_with_state.header.check_visibility(is_logged_in=True)

    @allure.story(Story.HEADER_NAVIGATION)
    @allure.severity(Severity.MAJOR)
    @allure.title("Навигация по ссылкам в хедере при неавторизованном состоянии")
    def test_header_navigation_links_unauthorized(self, home_page: HomePage):
        home_page.open_url(Route.Home)

        home_page.header.click_nav_link("login")
        home_page.check_url_exact(Route.Login)

        home_page.header.click_shop_logo()
        home_page.check_url_exact(Route.Home)

        home_page.header.click_nav_link("register")
        home_page.check_url_exact(Route.Registration)

        home_page.header.click_nav_link("home")
        home_page.check_url_exact(Route.Home)

    @allure.story(Story.HEADER_NAVIGATION)
    @allure.severity(Severity.MAJOR)
    @allure.title("Навигация по ссылкам в хедере при авторизованном состоянии")
    def test_header_navigation_links_authorized(self, home_page_with_state: HomePage):
        home_page_with_state.open_url(Route.Home)

        home_page_with_state.header.click_nav_link("cart")
        home_page_with_state.check_url_exact(Route.Cart)

        home_page_with_state.header.click_shop_logo()
        home_page_with_state.check_url_exact(Route.Home)

        home_page_with_state.header.click_nav_link("orders")
        home_page_with_state.check_url_exact(Route.OrdersList)

        home_page_with_state.header.click_nav_link("home")
        home_page_with_state.check_url_exact(Route.Home)

        home_page_with_state.header.click_user_profile_dropdown_button()
        home_page_with_state.header.click_dropdown_menu_link("profile")
        home_page_with_state.check_url_exact(Route.UserProfile)

        home_page_with_state.header.click_user_profile_dropdown_button()
        home_page_with_state.header.click_dropdown_menu_link("settings")
        home_page_with_state.check_url_matches(re.compile(r"/profile#settings"))

    @allure.story(Story.USER_LOGOUT)
    @allure.severity(Severity.NORMAL)
    @allure.title("Выход из аккаунта")
    def test_logout(self, home_page_with_state: HomePage):
        home_page_with_state.open_url(Route.Home)

        home_page_with_state.header.click_user_profile_dropdown_button()
        home_page_with_state.header.click_dropdown_menu_link("logout")
        home_page_with_state.check_success_logout_message()
        home_page_with_state.header.check_visibility()





