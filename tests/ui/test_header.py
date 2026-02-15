import re

import pytest

from src.ui.pages.home import HomePage
from src.ui.tools.routes import Route


@pytest.mark.ui
@pytest.mark.header
@pytest.mark.regression
class TestHeader:
    def test_header_visibility_unauthorized(self, home_page: HomePage):
        home_page.open_url(Route.Home)

        home_page.header.check_visibility()

    def test_header_visibility_authorized(self, home_page_with_state: HomePage):
        home_page_with_state.open_url(Route.Home)

        home_page_with_state.header.check_visibility(is_logged_in=True)

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

    def test_logout(self, home_page_with_state: HomePage):
        home_page_with_state.open_url(Route.Home)

        home_page_with_state.header.click_user_profile_dropdown_button()
        home_page_with_state.header.click_dropdown_menu_link("logout")
        home_page_with_state.check_success_logout_message()
        home_page_with_state.header.check_visibility()





