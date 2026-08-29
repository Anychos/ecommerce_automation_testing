from pathlib import Path

import pytest
from allure_commons import hookimpl, plugin_manager

from config import settings
from utils.allure.environment import create_allure_environment_file
from utils.allure.redaction import redact_parameters, sanitize_allure_results


class AllureRedactionPlugin:
    @hookimpl(tryfirst=True)
    def start_step(self, uuid, title, params) -> None:
        secret_values = (
            settings.admin_data.password,
            settings.test_user.password,
            settings.test_user.confirm_password,
        )
        redact_parameters(params, secret_values)


allure_redaction_plugin = AllureRedactionPlugin()


def pytest_configure(config) -> None:
    if not plugin_manager.is_registered(allure_redaction_plugin):
        plugin_manager.register(allure_redaction_plugin, "allure-redaction")


def pytest_unconfigure(config) -> None:
    if plugin_manager.is_registered(allure_redaction_plugin):
        plugin_manager.unregister(allure_redaction_plugin)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Сохраняет результаты фаз теста для условного прикрепления trace."""

    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus) -> None:
    config = session.config
    if hasattr(config, "workerinput"):
        return

    allure_results_dir = config.getoption("allure_report_dir")
    if not allure_results_dir:
        return

    sanitize_allure_results(
        Path(allure_results_dir),
        secret_values=(
            settings.admin_data.password,
            settings.test_user.password,
            settings.test_user.confirm_password,
        ),
    )


@pytest.fixture(scope="session", autouse=True)
def save_allure_environment_file(request):
    """
    Сохраняет информацию об окружении для Allure отчета
    """

    yield
    allure_results_dir = request.config.getoption("allure_report_dir")
    if allure_results_dir:
        create_allure_environment_file(Path(allure_results_dir))
