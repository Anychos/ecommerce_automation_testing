from http import HTTPStatus

import allure
import pytest

from src.api.clients.payments.client import PaymentsAPIClient
from src.api.clients.payments.schemas import (
    CreateOrderPaymentResponseSchema,
    FakeCancelPaymentResponseSchema,
    FakeSucceedPaymentResponseSchema,
    GetPaymentByIdResponseSchema,
)
from src.api.fixtures.deliveries import DeliveryFixture
from src.api.fixtures.order import OrderFixture
from src.api.fixtures.payments import PaymentFixture
from src.api.tools.assertions.base_assertions import assert_json_schema, assert_status_code
from src.api.tools.assertions.payments import (
    assert_cancel_payment_response,
    assert_create_payment_response,
    assert_get_payment_response,
    assert_succeed_payment_response,
)
from utils.allure.epic import Epic
from utils.allure.feature import Feature
from utils.allure.severity import Severity
from utils.allure.story import Story


@pytest.mark.api
@pytest.mark.regression
@allure.epic(Epic.BACKEND_API)
@allure.feature(Feature.USER_CHECKOUT)
class TestPaymentPositive:
    @pytest.mark.smoke
    @allure.story(Story.USER_CHECKOUT)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Создание оплаты после выбора доставки")
    def test_create_payment_success(
            self,
            private_payments_client: PaymentsAPIClient,
            create_order: OrderFixture,
            create_delivery: DeliveryFixture
    ) -> None:
        response = private_payments_client.create_order_payment_api(
            order_id=create_delivery.order_id
        )
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = CreateOrderPaymentResponseSchema.model_validate_json(response.text)
        assert_create_payment_response(
            actual=response_data,
            order=create_order.response,
            delivery=create_delivery.response
        )
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.story(Story.USER_CHECKOUT)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Получение оплаты по идентификатору")
    def test_get_payment_info_success(
            self,
            private_payments_client: PaymentsAPIClient,
            create_payment: PaymentFixture
    ) -> None:
        response = private_payments_client.get_payment_api(
            payment_id=create_payment.payment_id
        )
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = GetPaymentByIdResponseSchema.model_validate_json(response.text)
        assert_get_payment_response(actual=response_data, expected=create_payment.response)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.story(Story.USER_CHECKOUT)
    @allure.severity(Severity.NORMAL)
    @allure.title("Успешная fake-оплата")
    def test_fake_succeed_payment_success(
            self,
            private_payments_client: PaymentsAPIClient,
            create_payment: PaymentFixture
    ) -> None:
        response = private_payments_client.fake_succeed_payment_api(
            payment_id=create_payment.payment_id
        )
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = FakeSucceedPaymentResponseSchema.model_validate_json(response.text)
        assert_succeed_payment_response(actual=response_data, expected=create_payment.response)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.story(Story.USER_CHECKOUT)
    @allure.severity(Severity.NORMAL)
    @allure.title("Отмена fake-оплаты")
    def test_fake_cancel_payment_success(
            self,
            private_payments_client: PaymentsAPIClient,
            create_payment: PaymentFixture
    ) -> None:
        response = private_payments_client.fake_cancel_payment_api(
            payment_id=create_payment.payment_id
        )
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = FakeCancelPaymentResponseSchema.model_validate_json(response.text)
        assert_cancel_payment_response(actual=response_data, expected=create_payment.response)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())
