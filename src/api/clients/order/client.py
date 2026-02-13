import allure
from httpx import Response

from src.api.clients.api_coverage import tracker
from src.api.clients.authentication.schemas import LoginRequestSchema
from src.api.clients.base_client import BaseAPIClient
from src.api.clients.order.schemas import CreateOrderRequestSchema, CreateOrderResponseSchema
from src.api.clients.private_builder import private_user_client_builder
from src.api.clients.public_builder import public_client_builder
from src.api.tools.routes import Routes


class OrderAPIClient(BaseAPIClient):
    """
    Клиент для работы с API заказа
    """

    @tracker.track_coverage_httpx(Routes.ORDERS)
    @allure.step("Отправка запроса на создание заказа")
    def create_order_api(self,
                         *,
                         request: CreateOrderRequestSchema
                         ) -> Response:
        """
        Отправляет запрос на создание заказа

        :param request: Данные для создания заказа
        :return: Ответ сервера с данными созданного заказа
        """

        return self.post(url=Routes.ORDERS, json=request.model_dump())

    def create_order(self,
                     *,
                     request: CreateOrderRequestSchema
                     ) -> CreateOrderResponseSchema:
        response = self.create_order_api(request=request)
        return CreateOrderResponseSchema.model_validate_json(response.text)

    @tracker.track_coverage_httpx(f"{Routes.ORDERS}/" + "{order_id}")
    @allure.step("Отправка запроса на получение заказа")
    def get_order_api(self,
                      *,
                      order_id: int
                      ) -> Response:
        """
        Отправляет запрос на получение заказа

        :param order_id: Идентификатор заказа
        :return: Ответ сервера с данными заказа
        """

        return self.get(url=f"{Routes.ORDERS}/{order_id}")

    @tracker.track_coverage_httpx(Routes.ORDERS)
    @allure.step("Отправка запроса на получение заказов пользователя")
    def get_orders_api(self) -> Response:
        """
        Отправляет запрос на получение заказов пользователя

        :return: Ответ сервера со списком заказов
        """

        return self.get(url=Routes.ORDERS)


def get_public_order_client() -> OrderAPIClient:
    """
    Создает публичный HTTP клиент для доступа к API заказов

    :return: Публичный HTTP клиент
    """

    return OrderAPIClient(client=public_client_builder())

def get_private_order_client(
        *,
        user: LoginRequestSchema
) -> OrderAPIClient:
    """
    Создает приватный HTTP клиент для доступа к API заказов

    :param user: Данные пользователя для авторизации
    :return: Приватный HTTP клиент
    """

    return OrderAPIClient(client=private_user_client_builder(user=user))
