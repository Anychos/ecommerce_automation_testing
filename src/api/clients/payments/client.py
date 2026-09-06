from httpx import Response

from src.api.clients.authentication.schemas import LoginRequestSchema
from src.api.clients.base_client import BaseAPIClient
from src.api.clients.payments.schemas import CreateOrderPaymentResponseSchema
from src.api.clients.private_builder import private_user_client_builder
from src.api.clients.public_builder import public_client_builder
from src.api.tools.routes import Routes


class PaymentsAPIClient(BaseAPIClient):
    """Клиент для работы с API оплаты"""
    def create_order_payment_api(self, order_id: int) -> Response:
        """
        Отправляет запрос на создание оплаты для заказа

        :param order_id: Идентификатор заказа
        :return: Ответ сервера с данными созданной оплаты
        """
        return self.post(url=f"{Routes.ORDERS}/{order_id}{Routes.PAYMENTS}", json=None)

    def create_order_payment(self, order_id: int) -> CreateOrderPaymentResponseSchema:
        response = self.create_order_payment_api(order_id=order_id)
        return CreateOrderPaymentResponseSchema.model_validate_json(response.content)

    def get_payment_api(self, payment_id: int) -> Response:
        """
        Отправляет запрос на получение оплаты

        :param payment_id: Идентификатор оплаты
        :return: Ответ сервера с данными оплаты
        """
        return self.get(url=f"{Routes.PAYMENTS}/{payment_id}")

    def sync_payment(self, payment_id: int) -> Response:
        """
        Отправляет запрос на синхронизацию оплаты

        :param payment_id: Идентификатор оплаты
        :return: Ответ сервера с данными синхронизированной оплаты
        """
        return self.post(url=f"{Routes.PAYMENTS}/{payment_id}/sync", json=None)

    def return_payment_after_pay_api(self, payment_id: int) -> Response:
        """
        Отправляет запрос на возврат оплаты

        :param payment_id: Идентификатор оплаты
        :return: Ответ сервера с данными возврата оплаты
        """
        return self.get(url=f"{Routes.PAYMENTS}/return", params={"payment_id": payment_id})

    def get_fake_checkout_payment_api(self, payment_id: int) -> Response:
        """
        Отправляет запрос на получение статуса оплаты на фиктивном чекауте

        :param payment_id: Идентификатор оплаты
        :return: Ответ сервера с данными о статусе оплаты
        """
        return self.get(url=f"{Routes.PAYMENTS}/fake/checkout/{payment_id}")

    def fake_succeed_payment_api(self, payment_id: int) -> Response:
        """
        Отправляет запрос на имитацию успешной оплаты

        :param payment_id: Идентификатор оплаты
        :return: Ответ сервера с данными успешно оплаченного заказа
        """
        return self.post(url=f"{Routes.PAYMENTS}/fake/{payment_id}/succeed", json=None)

    def fake_cancel_payment_api(self, payment_id: int) -> Response:
        """
        Отправляет запрос на имитацию отмены оплаты

        :param payment_id: Идентификатор оплаты
        :return: Ответ сервера с данными отмененной оплаты
        """
        return self.post(url=f"{Routes.PAYMENTS}/fake/{payment_id}/cancel", json=None)


def get_public_payments_client() -> PaymentsAPIClient:
    """Создает HTTP клиент для доступа к публичному API оплаты"""
    return PaymentsAPIClient(client=public_client_builder())


def get_private_payments_client(
        *,
        user: LoginRequestSchema
) -> PaymentsAPIClient:
    """
    Создает HTTP клиент для доступа к приватному API оплаты

    :param user: Данные пользователя для авторизации
    """
    return PaymentsAPIClient(client=private_user_client_builder(user=user))
