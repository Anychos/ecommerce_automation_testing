from __future__ import annotations

from http import HTTPStatus
from typing import Callable, TYPE_CHECKING, Generator

from src.api.tools.data_generator import fake_ru

if TYPE_CHECKING:
    from src.api.fixtures.user import UserFixture

import pytest
from pydantic import BaseModel

from src.api.clients.product.client import ProductAPIClient, get_public_product_client, get_private_product_client
from src.api.clients.product.schemas import CreateProductRequestSchema, CreateProductResponseSchema, \
    FullUpdateProductRequestSchema, UpdateProductResponseSchema


class CreateProductFixture(BaseModel):
    """Хранит данные о созданном товаре"""
    request: CreateProductRequestSchema
    response: CreateProductResponseSchema

    @property
    def product_id(self) -> int:
        return self.response.id


class UpdateProductFixture(BaseModel):
    """Хранит данные об обновленном товаре"""
    request: FullUpdateProductRequestSchema
    response: UpdateProductResponseSchema

    @property
    def product_id(self) -> int:
        return self.response.id


@pytest.fixture
def public_product_client() -> Generator[ProductAPIClient, None, None]:
    """Возвращает готовый HTTP клиент для доступа к публичному API продукта"""
    client = get_public_product_client()

    try:
        yield client
    finally:
        client.close()

@pytest.fixture
def admin_private_product_client(admin: UserFixture) -> Generator[ProductAPIClient, None, None]:
    """
    Возвращает готовый HTTP клиент для доступа администратора к приватному API продукта

    :param admin: Созданный администратор
    """
    client = get_private_product_client(user=admin.user_schema)

    try:
        yield client
    finally:
        client.close()

@pytest.fixture
def user_private_product_client(user: UserFixture) -> Generator[ProductAPIClient, None, None]:
    """
    Возвращает готовый HTTP клиент для доступа пользователя к приватному API продукта

    :param user: Созданный пользователь
    :return: Приватный HTTP клиент пользователя для работы с API продукта
    """
    client = get_private_product_client(user=user.user_schema)

    try:
        yield client
    finally:
        client.close()

@pytest.fixture
def create_product_factory(admin_private_product_client: ProductAPIClient) -> Generator[
    Callable[..., CreateProductFixture], None, None]:
    """
    Возвращает фабрику для создания продукта

    :param admin_private_product_client: Приватный HTTP клиент для доступа к API продукта
    """
    created_products: list[CreateProductFixture] = []

    def _create_product(
            **overrides
    ) -> CreateProductFixture:
        """
        Создает продукт с указанными параметрами

        :return: Объект ProductFixture с информацией о продукте
        """
        request = CreateProductRequestSchema(
            **overrides
        )
        response = admin_private_product_client.create_product(request=request)

        product = CreateProductFixture(request=request, response=response)
        created_products.append(product)
        return product

    try:
        yield _create_product
    finally:
        cleanup_errors: list[Exception] = []

        for product in created_products:
            try:
                response = admin_private_product_client.delete_product_api(product_id=product.product_id)
                if not 200 <= response.status_code < 300 and response.status_code != HTTPStatus.NOT_FOUND:
                    cleanup_errors.append(
                        RuntimeError(
                            f"Не удалось удалить продукт {product.product_id}: "
                            f"HTTP {response.status_code} {response.reason_phrase}"
                        )
                    )
            except Exception as error:
                cleanup_errors.append(
                    RuntimeError(f"Не удалось удалить продукт {product.product_id}: {error}")
                )

        if cleanup_errors:
            raise ExceptionGroup("Ошибки очистки тестовых продуктов", cleanup_errors)

@pytest.fixture
def create_available_product(create_product_factory: Callable[..., CreateProductFixture]) -> CreateProductFixture:
    """
    Возвращает созданный продукт

    :param create_product_factory: Фабрика для создания продукта
    :return: Объект ProductFixture с информацией о продукте
    """
    return create_product_factory(is_available=True)

@pytest.fixture
def update_product_factory(admin_private_product_client: ProductAPIClient) -> Callable[..., UpdateProductFixture]:
    """
    Возвращает фабрику для обновления продукта

    :param admin_private_product_client: Приватный HTTP клиент для доступа к API продукта
    """
    def _update_product(
            product_id: int,
            **overrides,
    ) -> UpdateProductFixture:
        """
        Обновляет продукт с указанными параметрами

        :return: Объект ProductFixture с информацией об обновленном продукте
        """
        request = FullUpdateProductRequestSchema(
            **overrides,
        )
        response = admin_private_product_client.full_update_product(product_id=product_id, request=request)
        return UpdateProductFixture(request=request, response=response)

    return _update_product
