from http import HTTPStatus
from typing import Generator

import pytest
from httpx import RequestError

from src.api.clients.health.client import HealthCheckAPIClient, get_public_health_check_client
from src.api.clients.health.schema import HealthCheckResponseSchema


@pytest.fixture(scope="session")
def check_health_client() -> Generator[HealthCheckAPIClient, None, None]:
    """Возвращает готовый HTTP клиент для доступа к публичному API проверки работы сервера"""
    client = get_public_health_check_client()

    try:
        yield client
    finally:
        client.close()

@pytest.fixture(scope="session", autouse=True)
def check_environment_is_ready(check_health_client: HealthCheckAPIClient) -> None:
    try:
        response = check_health_client.health_check_api()
    except RequestError as error:
        pytest.exit(f"Окружение недоступно: {error}")

    if response.status_code != HTTPStatus.OK:
        pytest.exit(
            f"Окружение недоступно: "
            f"Получен статус код {response.status_code}"
        )

    HealthCheckResponseSchema.model_validate_json(response.content)
