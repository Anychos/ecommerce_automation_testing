from enum import Enum
from typing import Self

from pydantic import BaseModel, DirectoryPath, FilePath, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Browser(str, Enum):
    CHROME = "chromium"
    FIREFOX = "firefox"
    SAFARI = "webkit"


class BrowserViewport(BaseModel):
    width: int
    height: int
    device_scale_factor: float = 1.0


class TestUserData(BaseModel):
    email: str
    name: str
    phone: str
    password: str
    confirm_password: str


class HTTPClientSettings(BaseModel):
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


class APISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__"
    )
    http_client: HTTPClientSettings
    swagger_coverage_services: list[SwaggerService]
    admin_data: AdminLoginSchema
    expired_user_token: str
    expired_admin_token: str


class UISettings(APISettings):
    base_url: HttpUrl
    headless: bool
    browser: list[Browser]
    browser_viewport: BrowserViewport
    session_browser_state_file: FilePath
    function_browser_state_file: FilePath
    test_user: TestUserData


class Settings(UISettings):
    allure_results_dir: DirectoryPath = DirectoryPath("allure-results")

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
            allure_results_dir=allure_results_dir,
        )


settings = Settings.init()
