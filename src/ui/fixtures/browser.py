import allure
import pytest
from hashlib import sha256
from pathlib import Path
from _pytest.fixtures import SubRequest
from playwright.sync_api import BrowserContext, Page, Playwright

from config import settings
from src.ui.models.user_data import UserData
from src.ui.pages.home import HomePage
from src.ui.pages.registration import RegistrationPage
from src.ui.tools.routes import Route


def _trace_path(request: SubRequest) -> Path:
    digest = sha256(request.node.nodeid.encode("utf-8")).hexdigest()[:12]
    return Path("tracing", f"{request.node.name}-{digest}.zip")


def _stop_trace_and_attach_on_failure(
        context: BrowserContext,
        request: SubRequest
        ) -> None:
    trace_path = _trace_path(request)
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    context.tracing.stop(path=trace_path)

    reports = (
        getattr(request.node, "rep_setup", None),
        getattr(request.node, "rep_call", None),
        getattr(request.node, "rep_teardown", None),
    )
    if any(report is not None and report.failed for report in reports):
        allure.attach.file(
            trace_path,
            name=f"trace - {request.node.name}",
            extension="zip",
        )
        return

    trace_path.unlink(missing_ok=True)
    try:
        trace_path.parent.rmdir()
    except OSError:
        pass


@pytest.fixture
def chromium_page(request: SubRequest, playwright: Playwright) -> Page:
    """
    Запускает Chromium браузер и открывает страницу приложения

    :param request: Объект запроса Pytest
    :param playwright: Экземпляр Playwright, предоставляемый pytest-playwright
    :return: Объект Page для взаимодействия со страницей
    """

    browser = playwright.chromium.launch(headless=settings.headless)
    context = browser.new_context(base_url=settings.get_base_url(),
                                  viewport=settings.browser_viewport.model_dump()
                                  )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    yield page
    try:
        _stop_trace_and_attach_on_failure(context, request)
    finally:
        context.close()
        browser.close()


@pytest.fixture(scope="session")
def session_get_browser_state(playwright: Playwright) -> None:
    """
    Запускает Chromium браузер, создает и сохраняет состояние браузера зарегистрированного пользователя

    :param playwright: Экземпляр Playwright, предоставляемый pytest-playwright
    :return: Файл с состоянием браузера
    """

    browser = playwright.chromium.launch(headless=settings.headless)
    context = browser.new_context(base_url=settings.get_base_url())
    page = context.new_page()
    registration_page = RegistrationPage(page)
    home_page = HomePage(page)

    registration_page.open_url(Route.Registration)
    registration_page.registration_form.fill(
        email=settings.test_user.email,
        name=settings.test_user.name,
        phone=settings.test_user.phone,
        password=settings.test_user.password,
        confirm_password=settings.test_user.confirm_password
    )
    registration_page.registration_form.click_registration_button()
    home_page.check_success_registration_message()

    context.storage_state(path=settings.session_browser_state_file)

    context.close()
    browser.close()


@pytest.fixture
def function_get_browser_state(playwright: Playwright, user_data_function: UserData) -> None:
    """
    Запускает Chromium браузер, создает и сохраняет состояние браузера зарегистрированного пользователя

    :param playwright: Экземпляр Playwright, предоставляемый pytest-playwright
    :param user_data_function: Данные пользователя для регистрации
    :return: Файл с состоянием браузера
    """

    browser = playwright.chromium.launch(headless=settings.headless)
    context = browser.new_context(base_url=settings.get_base_url())
    page = context.new_page()
    registration_page = RegistrationPage(page)
    home_page = HomePage(page)

    registration_page.open_url(Route.Registration)
    registration_page.registration_form.fill(
        email=user_data_function.email,
        name=user_data_function.name,
        phone=user_data_function.phone,
        password=user_data_function.password,
        confirm_password=user_data_function.confirm_password
    )
    registration_page.registration_form.click_registration_button()
    home_page.check_success_registration_message()

    context.storage_state(path=settings.function_browser_state_file)

    context.close()
    browser.close()


@pytest.fixture
def session_chromium_page_with_state(request: SubRequest, session_get_browser_state, playwright: Playwright) -> Page:
    """
    Запускает Chromium браузер и открывает страницу приложения с сохраненным состоянием

    :param request: Объект запроса Pytest
    :param session_get_browser_state: Функция, создающая и сохраняющая состояние браузера
    :param playwright: Экземпляр Playwright, предоставляемый pytest-playwright
    :return: Объект Page для взаимодействия со страницей
    """

    browser = playwright.chromium.launch(headless=settings.headless)
    context = browser.new_context(
        base_url=settings.get_base_url(),
        storage_state=settings.session_browser_state_file,
        viewport=settings.browser_viewport.model_dump()
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    yield page
    try:
        _stop_trace_and_attach_on_failure(context, request)
    finally:
        context.close()
        browser.close()


@pytest.fixture
def function_chromium_page_with_state(request: SubRequest, function_get_browser_state, playwright: Playwright) -> Page:
    """
    Запускает Chromium браузер и открывает страницу приложения с сохраненным состоянием

    :param request: Объект запроса Pytest
    :param function_get_browser_state: Функция, создающая и сохраняющая состояние браузера
    :param playwright: Экземпляр Playwright, предоставляемый pytest-playwright
    :return: Объект Page для взаимодействия со страницей
    """

    browser = playwright.chromium.launch(headless=settings.headless)
    context = browser.new_context(
        base_url=settings.get_base_url(),
        storage_state=settings.function_browser_state_file,
        viewport=settings.browser_viewport.model_dump()
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    yield page
    try:
        _stop_trace_and_attach_on_failure(context, request)
    finally:
        context.close()
        browser.close()
