from httpx import Response

from src.api.clients.base_client import BaseAPIClient
from src.api.tools.routes import Routes


class DeliveriesAPIClient(BaseAPIClient):
    def quote_delivery_api(self) -> Response:
        return self.client.post(url=Routes.DELIVERIES)
