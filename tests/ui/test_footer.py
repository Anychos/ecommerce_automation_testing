import allure
import pytest

from utils.allure.epic import Epic


@pytest.mark.ui
@pytest.mark.footer
@pytest.mark.regression
@allure.epic(Epic.STORE_FRONT)
class TestFooter:
    pass
