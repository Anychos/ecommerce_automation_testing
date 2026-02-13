from enum import Enum
from typing import List
from typing import Self

from pydantic import BaseModel, HttpUrl, DirectoryPath
from pydantic import FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Browser(str, Enum):
    CHROME = "chromium"
    FIREFOX = "firefox"
    SAFARI = "webkit"


class TestUser(BaseModel):
    email: str
    name: str
    phone: str
    password: str
    confirm_password: str


class TestUserLogin(BaseModel):
    email: str
    password: str


class HTTPClientSettings(BaseModel):
    """
    Настройки HTTP клиента
    """
    base_url: HttpUrl
    timeout: int

    @property
    def url(self) -> str:
        return str(self.base_url)


class AdminLoginSchema(BaseModel):
    email: str
    password: str


class SwaggerService(BaseModel):
    key: str
    name: str
    repository: HttpUrl
    swagger_url: HttpUrl


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="."
    )

    base_url: HttpUrl
    headless: bool
    browser: List[Browser]
    session_browser_state_file: FilePath
    function_browser_state_file: FilePath
    test_user: TestUser
    test_user_login: TestUserLogin
    http_client: HTTPClientSettings
    allure_results_dir: DirectoryPath = DirectoryPath("allure-results")
    admin_data: AdminLoginSchema
    swagger_coverage_services: List[SwaggerService]

    def get_base_url(self) -> str:
        return str(self.base_url)

    @classmethod
    def init(cls) -> Self:
        session_browser_state_file = FilePath("session-browser-state.json")
        function_browser_state_file = FilePath("function-browser-state.json")
        allure_results_dir = DirectoryPath("./allure-results")

        session_browser_state_file.touch(exist_ok=True)
        function_browser_state_file.touch(exist_ok=True)
        allure_results_dir.mkdir(exist_ok=True)

        return Settings(
            session_browser_state_file=session_browser_state_file,
            function_browser_state_file=function_browser_state_file,
            allure_results_dir=allure_results_dir
        )


settings = Settings.init()
