from http import HTTPStatus

import allure
import pytest

from src.api.clients.deliveries.client import DeliveriesAPIClient
from src.api.clients.deliveries.schemas import (
    CreateOrderDeliveryRequestSchema,
    CreateOrderDeliveryResponseSchema,
    FakeAssignDeliveryResponseSchema,
    FakeCancelDeliveryResponseSchema,
    FakeDeliverDeliveryResponseSchema,
    FakePickupDeliveryResponseSchema,
    GetDeliveryByIdResponseResponseSchema,
)
from src.api.fixtures.deliveries import DeliveryFixture
from src.api.fixtures.order import OrderFixture
from src.api.clients.payments.client import PaymentsAPIClient
from src.api.clients.payments.schemas import FakeSucceedPaymentResponseSchema
from src.api.fixtures.payments import PaymentFixture
from src.api.tools.assertions.base_assertions import assert_json_schema, assert_status_code
from src.api.tools.assertions.deliveries import (
    assert_assigned_delivery,
    assert_canceled_delivery,
    assert_create_order_delivery_response,
    assert_delivered_delivery,
    assert_get_delivery_response,
    assert_picked_delivery,
)
from src.api.tools.assertions.payments import assert_succeed_payment_response
from utils.allure.epic import Epic
from utils.allure.feature import Feature
from utils.allure.severity import Severity
from utils.allure.story import Story


def _activate_delivery(
        *,
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


@pytest.mark.api
@pytest.mark.regression
@allure.epic(Epic.BACKEND_API)
@allure.feature(Feature.USER_CHECKOUT)
class TestDeliveryPositive:
    @pytest.mark.smoke
    @allure.story(Story.USER_CHECKOUT)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Создание доставки для заказа")
    def test_create_delivery_success(
            self,
            private_delivery_client: DeliveriesAPIClient,
            create_order: OrderFixture
    ) -> None:
        order_id = create_order.order_id
        request = CreateOrderDeliveryRequestSchema()

        response = private_delivery_client.create_order_delivery_api(
            order_id=order_id,
            request=request
        )
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = CreateOrderDeliveryResponseSchema.model_validate_json(response.text)
        assert_create_order_delivery_response(
            actual=response_data,
            expected=request,
            order_id=order_id
        )
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.story(Story.USER_CHECKOUT)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Получение доставки по идентификатору")
    def test_get_delivery_info_success(
            self,
            private_delivery_client: DeliveriesAPIClient,
            create_delivery: DeliveryFixture
    ) -> None:
        response = private_delivery_client.get_delivery_api(
            delivery_id=create_delivery.delivery_id
        )
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = GetDeliveryByIdResponseResponseSchema.model_validate_json(response.text)
        assert_get_delivery_response(actual=response_data, expected=create_delivery.response)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.story(Story.USER_CHECKOUT)
    @allure.severity(Severity.NORMAL)
    @allure.title("Назначение курьера для доставки")
    def test_fake_assign_delivery_success(
            self,
            private_delivery_client: DeliveriesAPIClient,
            private_payments_client: PaymentsAPIClient,
            create_payment: PaymentFixture
    ) -> None:
        _activate_delivery(
            private_payments_client=private_payments_client,
            create_payment=create_payment
        )

        response = private_delivery_client.fake_assign_delivery_api(
            delivery_id=create_payment.delivery.delivery_id
        )
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = FakeAssignDeliveryResponseSchema.model_validate_json(response.text)
        assert_assigned_delivery(actual=response_data, expected=create_payment.delivery.response)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.story(Story.USER_CHECKOUT)
    @allure.severity(Severity.NORMAL)
    @allure.title("Получение доставки курьером")
    def test_fake_pickup_delivery_success(
            self,
            private_delivery_client: DeliveriesAPIClient,
            private_payments_client: PaymentsAPIClient,
            create_payment: PaymentFixture
    ) -> None:
        _activate_delivery(
            private_payments_client=private_payments_client,
            create_payment=create_payment
        )

        assign_response = private_delivery_client.fake_assign_delivery_api(
            delivery_id=create_payment.delivery.delivery_id
        )
        assert_status_code(assign_response.status_code, HTTPStatus.OK)

        assign_response_data = FakeAssignDeliveryResponseSchema.model_validate_json(assign_response.text)
        assert_assigned_delivery(actual=assign_response_data, expected=create_payment.delivery.response)
        assert_json_schema(actual=assign_response.json(), schema=assign_response_data.model_json_schema())

        response = private_delivery_client.fake_pickup_delivery_api(
            delivery_id=create_payment.delivery.delivery_id
        )
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = FakePickupDeliveryResponseSchema.model_validate_json(response.text)
        assert_picked_delivery(actual=response_data, expected=assign_response_data)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.story(Story.USER_CHECKOUT)
    @allure.severity(Severity.NORMAL)
    @allure.title("Доставка заказа курьером")
    def test_fake_deliver_delivery_success(
            self,
            private_delivery_client: DeliveriesAPIClient,
            private_payments_client: PaymentsAPIClient,
            create_payment: PaymentFixture
    ) -> None:
        _activate_delivery(
            private_payments_client=private_payments_client,
            create_payment=create_payment
        )

        assign_response = private_delivery_client.fake_assign_delivery_api(
            delivery_id=create_payment.delivery.delivery_id
        )
        assert_status_code(assign_response.status_code, HTTPStatus.OK)

        assign_response_data = FakeAssignDeliveryResponseSchema.model_validate_json(assign_response.text)
        assert_assigned_delivery(actual=assign_response_data, expected=create_payment.delivery.response)
        assert_json_schema(actual=assign_response.json(), schema=assign_response_data.model_json_schema())

        pickup_response = private_delivery_client.fake_pickup_delivery_api(
            delivery_id=create_payment.delivery.delivery_id
        )
        assert_status_code(pickup_response.status_code, HTTPStatus.OK)

        pickup_response_data = FakePickupDeliveryResponseSchema.model_validate_json(pickup_response.text)
        assert_picked_delivery(actual=pickup_response_data, expected=assign_response_data)
        assert_json_schema(actual=pickup_response.json(), schema=pickup_response_data.model_json_schema())

        response = private_delivery_client.fake_deliver_delivery_api(
            delivery_id=create_payment.delivery.delivery_id
        )
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = FakeDeliverDeliveryResponseSchema.model_validate_json(response.text)
        assert_delivered_delivery(actual=response_data, expected=pickup_response_data)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.story(Story.USER_CHECKOUT)
    @allure.severity(Severity.NORMAL)
    @allure.title("Отмена доставки")
    def test_fake_cancel_delivery_success(
            self,
            private_delivery_client: DeliveriesAPIClient,
            private_payments_client: PaymentsAPIClient,
            create_payment: PaymentFixture
    ) -> None:
        _activate_delivery(
            private_payments_client=private_payments_client,
            create_payment=create_payment
        )

        assign_response = private_delivery_client.fake_assign_delivery_api(
            delivery_id=create_payment.delivery.delivery_id
        )
        assert_status_code(assign_response.status_code, HTTPStatus.OK)

        assign_response_data = FakeAssignDeliveryResponseSchema.model_validate_json(assign_response.text)
        assert_assigned_delivery(actual=assign_response_data, expected=create_payment.delivery.response)
        assert_json_schema(actual=assign_response.json(), schema=assign_response_data.model_json_schema())

        response = private_delivery_client.fake_cancel_delivery_api(
            delivery_id=create_payment.delivery.delivery_id
        )
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = FakeCancelDeliveryResponseSchema.model_validate_json(response.text)
        assert_canceled_delivery(actual=response_data, expected=assign_response_data)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())
