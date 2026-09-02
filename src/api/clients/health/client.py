from httpx import Response

from src.api.clients.base_client import BaseAPIClient
from src.api.clients.health.schema import HealthCheckResponseSchema
from src.api.clients.public_builder import public_client_builder
from src.api.tools.routes import Routes


class HealthCheckAPIClient(BaseAPIClient):
    def health_check_api(self) -> Response:
        return self.client.get(url=Routes.HEALTH)

    def health_check(self) -> HealthCheckResponseSchema:
        response = self.health_check_api()
        return HealthCheckResponseSchema.model_validate_json(response.content)


def get_public_health_check_client() -> HealthCheckAPIClient:
    """Создает HTTP клиент для доступа к публичному API проверки состояния сервера"""
    return HealthCheckAPIClient(client=public_client_builder())