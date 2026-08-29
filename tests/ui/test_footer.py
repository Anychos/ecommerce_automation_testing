import allure
import pytest

from src.ui.pages.home import HomePage
from src.ui.tools.routes import Route
from utils.allure.epic import Epic
from utils.allure.severity import Severity
from utils.allure.story import Story


@pytest.mark.ui
@pytest.mark.footer
@pytest.mark.regression
@allure.epic(Epic.STORE_FRONT)
class TestFooter:
    @allure.story(Story.PAGE_VISIBILITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Отображение футера на главной странице")
    def test_footer_visibility(self, home_page: HomePage) -> None:
        home_page.open_url(Route.Home)

        home_page.footer.check_visibility()
