from httpx import Response

from src.api.clients.authentication.schemas import LoginRequestSchema
from src.api.clients.base_client import BaseAPIClient
from src.api.clients.deliveries.schemas import CreateOrderDeliveryRequestSchema, QuoteRequestSchema, \
    CreateOrderDeliveryResponseSchema
from src.api.clients.private_builder import private_user_client_builder
from src.api.clients.public_builder import public_client_builder
from src.api.tools.routes import Routes


class DeliveriesAPIClient(BaseAPIClient):
    """Клиент для работы с API доставки"""
    def quote_delivery_api(self, request: QuoteRequestSchema) -> Response:
        """
        Отправляет запрос на получение стоимости доставки

        :param request: Данные для создания доставки
        :return: Ответ сервера со стоимостью доставки
        """
        return self.post(url=f"{Routes.DELIVERIES}/quote", json=request.model_dump())

    def create_order_delivery_api(self, order_id: int, request: CreateOrderDeliveryRequestSchema) -> Response:
        """
        Отправляет запрос на создание доставки для заказа

        :param request: Данные для создания доставки
        :param order_id: Идентификатор заказа
        :return: Ответ сервера с данными созданной доставки
        """
        return self.post(url=f"{Routes.ORDERS}/{order_id}{Routes.DELIVERIES}", json=request.model_dump())

    def create_order_delivery(self, order_id: int, request: CreateOrderDeliveryRequestSchema) -> CreateOrderDeliveryResponseSchema:
        response = self.create_order_delivery_api(order_id=order_id, request=request)
        return CreateOrderDeliveryResponseSchema.model_validate_json(response.content)

    def get_delivery_api(self, delivery_id: int) -> Response:
        """
        Отправляет запрос на получение доставки

        :param delivery_id: Идентификатор доставки
        :return: Ответ сервера с данными доставки
        """
        return self.get(url=f"{Routes.DELIVERIES}/{delivery_id}")

    def sync_delivery_api(self, delivery_id: int) -> Response:
        """
        Отправляет запрос на синхронизацию доставки

        :param delivery_id: Идентификатор доставки
        :return: Ответ сервера с данными синхронизированной доставки
        """
        return self.post(url=f"{Routes.DELIVERIES}/{delivery_id}/sync")

    def fake_assign_delivery_api(self, delivery_id: int) -> Response:
        """
        Отправляет запрос на имитацию назначения курьера на доставку

        :param delivery_id: Идентификатор доставки
        :return: Ответ сервера с данными доставки с назначенным курьером
        """
        return self.post(url=f"{Routes.DELIVERIES}/fake/{delivery_id}/assign", json=None)

    def fake_pickup_delivery_api(self, delivery_id: int) -> Response:
        """
        Отправляет запрос на имитацию получения доставки курьером

        :param delivery_id: Идентификатор доставки
        :return: Ответ сервера с данными полученной доставки
        """
        return self.post(url=f"{Routes.DELIVERIES}/fake/{delivery_id}/pickup", json=None)

    def fake_deliver_delivery_api(self, delivery_id: int) -> Response:
        """
        Отправляет запрос на имитацию доставки заказа

        :param delivery_id: Идентификатор доставки
        :return: Ответ сервера с данными доставленного заказа
        """
        return self.post(url=f"{Routes.DELIVERIES}/fake/{delivery_id}/deliver", json=None)

    def fake_cancel_delivery_api(self, delivery_id: int) -> Response:
        """
        Отправляет запрос на имитацию отмены доставки

        :param delivery_id: Идентификатор доставки
        :return: Ответ сервера с данными отмененной доставки
        """
        return self.post(url=f"{Routes.DELIVERIES}/fake/{delivery_id}/cancel", json=None)


def get_public_deliveries_client() -> DeliveriesAPIClient:
    """Создает HTTP клиент для доступа к публичному API доставки"""
    return DeliveriesAPIClient(client=public_client_builder())


def get_private_deliveries_client(
        *,
        user: LoginRequestSchema
) -> DeliveriesAPIClient:
    """
    Создает HTTP клиент для доступа к приватному API доставки

    :param user: Данные пользователя для авторизации
    """
    return DeliveriesAPIClient(client=private_user_client_builder(user=user))
