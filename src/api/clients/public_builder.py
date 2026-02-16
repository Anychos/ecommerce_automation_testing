from httpx import Client

from config import settings
from src.api.clients.event_hooks import request_curl_event_hook


def public_client_builder() -> Client:
    """
    Создает HTTP клиент для доступа к публичному API

    :return: Публичный HTTP клиент
    """

    return Client(
        base_url=settings.http_client.url,
        timeout=settings.http_client.timeout,
        event_hooks={"request": [request_curl_event_hook]}
    )
