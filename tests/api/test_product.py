from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.api.fixtures.product import CreateProductFixture

import allure
import pytest
from pydantic import TypeAdapter

from src.api.clients.error_shemas import InputValidationErrorResponseSchema
from src.api.clients.product.client import ProductAPIClient
from src.api.clients.product.schemas import CreateProductRequestSchema, CreateProductResponseSchema, \
    GetProductResponseSchema, \
    FullUpdateProductRequestSchema, UpdateProductResponseSchema, DeleteProductResponseSchema, \
    PartialUpdateProductRequestSchema, GetProductsResponseSchema
from utils.allure.epic import Epic
from utils.allure.feature import Feature
from utils.allure.severity import Severity
from utils.allure.story import Story
from src.api.tools.assertions.base_assertions import assert_status_code, assert_json_schema
from src.api.tools.assertions.product import assert_create_product_response, assert_get_product_response, \
    assert_full_update_product_response, assert_delete_product_response, assert_wrong_data_format_response, \
    assert_empty_required_field_response, assert_partial_update_product_response, assert_invalid_image_url_response, \
    assert_get_products_response
from src.api.tools.data_generator import fake_ru


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.product
@allure.epic(Epic.BACKEND_API)
class TestProductPositive:
    @pytest.mark.smoke
    @allure.feature(Feature.ADMIN_PRODUCTS)
    @allure.story(Story.ADMIN_CREATE_PRODUCT)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Создание продукта с валидными данными")
    def test_create_product(self, admin_private_product_client: ProductAPIClient) -> None:
        request = CreateProductRequestSchema()

        response = admin_private_product_client.create_product_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = CreateProductResponseSchema.model_validate_json(response.text)
        assert_create_product_response(actual=response_data, expected=request)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @pytest.mark.smoke
    @allure.feature(Feature.USER_PRODUCTS)
    @allure.story(Story.USER_GET_PRODUCT_BY_ID)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Получение существующего продукта")
    def test_get_product(self,
                         user_private_product_client: ProductAPIClient,
                         create_available_product: CreateProductFixture
                         ) -> None:
        response = user_private_product_client.get_product_api(product_id=create_available_product.product_id)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = GetProductResponseSchema.model_validate_json(response.text)
        assert_get_product_response(actual=response_data, expected=create_available_product.response)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @pytest.mark.smoke
    @allure.feature(Feature.USER_PRODUCTS)
    @allure.story(Story.USER_GET_PRODUCTS_LIST)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Получение списка продуктов")
    def test_get_products(self,
                          user_private_product_client: ProductAPIClient,
                          create_available_product: CreateProductFixture
                          ) -> None:
        response = user_private_product_client.get_products_api()
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = TypeAdapter(GetProductsResponseSchema).validate_json(response.text)
        assert_get_products_response(
            get_products_response=response_data,
            create_product_responses=[create_available_product.response]
        )
        product_schema = TypeAdapter(GetProductsResponseSchema).json_schema()
        assert_json_schema(actual=response.json(), schema=product_schema)

    @allure.feature(Feature.ADMIN_PRODUCTS)
    @allure.story(Story.ADMIN_UPDATE_PRODUCT_FULL)
    @allure.severity(Severity.NORMAL)
    @allure.title("Полное обновление существующего продукта")
    def test_full_update_product(self,
                            admin_private_product_client: ProductAPIClient,
                            create_available_product: CreateProductFixture
                            ) -> None:
        request = FullUpdateProductRequestSchema()

        response = admin_private_product_client.full_update_product_api(product_id=create_available_product.product_id, request=request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = UpdateProductResponseSchema.model_validate_json(response.text)
        assert_full_update_product_response(actual=response_data, expected=request)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.feature(Feature.ADMIN_PRODUCTS)
    @allure.story(Story.ADMIN_UPDATE_PRODUCT_PARTIAL)
    @allure.severity(Severity.NORMAL)
    @allure.title("Частичное обновление существующего продукта")
    def test_partial_update_product(self,
                                 admin_private_product_client: ProductAPIClient,
                                 create_available_product: CreateProductFixture
                                 ) -> None:
        request = PartialUpdateProductRequestSchema(name=fake_ru.first_name())

        response = admin_private_product_client.partial_update_product_api(product_id=create_available_product.product_id, request=request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = UpdateProductResponseSchema.model_validate_json(response.text)
        assert_partial_update_product_response(actual=response_data, expected=request)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.feature(Feature.ADMIN_PRODUCTS)
    @allure.story(Story.ADMIN_DELETE_PRODUCT)
    @allure.severity(Severity.NORMAL)
    @allure.title("Удаление существующего продукта")
    def test_delete_product(self,
                            admin_private_product_client: ProductAPIClient,
                            create_available_product: CreateProductFixture
                            ) -> None:
        response = admin_private_product_client.delete_product_api(product_id=create_available_product.product_id)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = DeleteProductResponseSchema.model_validate_json(response.text)
        assert_delete_product_response(response_data)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.product
@allure.epic(Epic.BACKEND_API)
class TestProductNegative:
    @allure.feature(Feature.ADMIN_PRODUCTS)
    @allure.story(Story.ADMIN_CREATE_PRODUCT)
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize("name, description, price, wrong_field, wrong_value",
                             [
                                 (123456, fake_ru.description(), fake_ru.price(), "name", 123456),
                                 (fake_ru.object_name(), 123456, fake_ru.price(), "description", 123456),
                                 (fake_ru.object_name(), fake_ru.description(), "price", "price", "price")
                             ],
                             ids=[
                                 "name - int",
                                 "description - int",
                                 "price - string"
                             ]
                             )
    @allure.title("Создание продукта с данными в невалидном формате")
    def test_create_product_wrong_data_format(self,
                                              admin_private_product_client: ProductAPIClient,
                                              name,
                                              description,
                                              price,
                                              wrong_field: str,
                                              wrong_value
                                              ) -> None:
        request = CreateProductRequestSchema.model_construct(
            name=name,
            description=description,
            price=price
        )

        response = admin_private_product_client.create_product_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        response_data = InputValidationErrorResponseSchema.model_validate_json(response.text)
        assert_wrong_data_format_response(
            actual=response_data,
            wrong_field=wrong_field,
            wrong_value=wrong_value
        )
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.feature(Feature.ADMIN_PRODUCTS)
    @allure.story(Story.ADMIN_CREATE_PRODUCT)
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize("name, description, price, image_url, wrong_field, wrong_value",
                             [
                                 ("", fake_ru.description(), fake_ru.price(), fake_ru.image_url(), "name", ""),
                                 (fake_ru.object_name(), "", fake_ru.price(), fake_ru.image_url(), "description", ""),
                                 (fake_ru.object_name(), fake_ru.description(), 0, fake_ru.image_url(), "price", 0),
                                 (fake_ru.object_name(), fake_ru.description(), fake_ru.price(), "", "image_url", "")
                             ],
                             ids=[
                                 "name - empty",
                                 "description - empty",
                                 "price - zero",
                                 "image_url - empty"
                             ]
                             )
    @allure.title("Создание продукта без заполнения обязательного поля")
    def test_create_product_empty_required_field(self,
                                                 admin_private_product_client: ProductAPIClient,
                                                 name,
                                                 description,
                                                 price,
                                                 image_url,
                                                 wrong_field: str,
                                                 wrong_value
                                                 ) -> None:
        request = CreateProductRequestSchema.model_construct(
            name=name,
            description=description,
            price=price,
            image_url=image_url
        )

        response = admin_private_product_client.create_product_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        response_data = InputValidationErrorResponseSchema.model_validate_json(response.text)
        assert_empty_required_field_response(actual=response_data, wrong_field=wrong_field, wrong_value=wrong_value)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @pytest.mark.parametrize("image_url",
                             ["example.com/image.jpg",
                              "https://example.com/image.gif"]
                             )
    @allure.feature(Feature.ADMIN_PRODUCTS)
    @allure.story(Story.ADMIN_CREATE_PRODUCT)
    @allure.severity(Severity.NORMAL)
    @allure.title("Создание продукта с некорректным URL изображения")
    def test_create_product_with_wrong_image_url(self,
                                                 admin_private_product_client: ProductAPIClient,
                                                 image_url: str
                                                 ) -> None:
        request = CreateProductRequestSchema(image_url=image_url)

        response = admin_private_product_client.create_product_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        response_data = InputValidationErrorResponseSchema.model_validate_json(response.text)
        assert_invalid_image_url_response(actual=response_data, image_url=image_url)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())
