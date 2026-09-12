from httpx import Client

from config import settings
from src.api.clients.authentication.schemas import LoginRequestSchema
from src.api.clients.event_hooks import request_curl_event_hook


def private_client_builder(
    *,
    user: LoginRequestSchema | None = None,
    token: str | None = None,
) -> Client:
    """Создает авторизованный HTTP клиент."""
    if user is None and token is None:
        raise ValueError("Необходимо передать user или token")

    if user is not None and token is not None:
        raise ValueError("Необходимо передать только user или token")

    if token is None:
        assert user is not None
        from src.api.clients.authentication.client import get_authentication_client

        auth_client = get_authentication_client()

        try:
            response = auth_client.login(request=user)
            token = response.access_token
        finally:
            auth_client.close()

    return Client(
        base_url=settings.http_client.url,
        timeout=settings.http_client.timeout,
        headers={"Authorization": f"Bearer {token}"},
        event_hooks={"request": [request_curl_event_hook]},
    )
