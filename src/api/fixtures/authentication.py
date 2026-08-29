from typing import Any, Generator

import pytest

from src.api.clients.authentication.client import AuthenticationAPIClient, get_authentication_client


@pytest.fixture
def auth_client() -> Generator[AuthenticationAPIClient, None, None]:
    """Возвращает готовый HTTP клиент для доступа к API аутентификации"""
    client = get_authentication_client()

    try:
        yield client
    finally:
        client.close()
