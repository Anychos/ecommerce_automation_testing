from __future__ import annotations

from typing import Callable, TYPE_CHECKING, Any, Generator

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
            *,
            is_available: bool = True,
            stock_quantity: int = 5,
            price: float = 500
    ) -> CreateProductFixture:
        """
        Создает продукт с указанными параметрами

        :return: Объект ProductFixture с информацией о продукте
        """
        request = CreateProductRequestSchema(
            is_available=is_available,
            stock_quantity=stock_quantity,
            price=price
        )
        response = admin_private_product_client.create_product(request=request)

        product = CreateProductFixture(request=request, response=response)
        created_products.append(product)
        return product

    yield _create_product

    for product in created_products:
        admin_private_product_client.delete_product_api(product_id=product.product_id)

@pytest.fixture
def create_available_product(create_product_factory: Callable[..., CreateProductFixture]) -> CreateProductFixture:
    """
    Возвращает созданный продукт

    :param create_product_factory: Фабрика для создания продукта
    :return: Объект ProductFixture с информацией о продукте
    """
    return create_product_factory()

@pytest.fixture
def update_product_factory(admin_private_product_client: ProductAPIClient) -> Callable[..., UpdateProductFixture]:
    """
    Возвращает фабрику для обновления продукта

    :param admin_private_product_client: Приватный HTTP клиент для доступа к API продукта
    """
    def _update_product(
            *,
            product_id: int,
            description: str = fake_ru.description(),
            image_url: str = fake_ru.image_url(),
            category: str = fake_ru.category(),
            is_available: bool = True,
            name: str = fake_ru.product_name(),
            price: float = fake_ru.price(),
            stock_quantity: int = 2
    ) -> UpdateProductFixture:
        """
        Обновляет продукт с указанными параметрами

        :return: Объект ProductFixture с информацией об обновленном продукте
        """
        request = FullUpdateProductRequestSchema(
            description=description,
            image_url=image_url,
            category=category,
            name=name,
            price=price,
            is_available=is_available,
            stock_quantity=stock_quantity
        )
        response = admin_private_product_client.full_update_product(product_id=product_id, request=request)
        return UpdateProductFixture(request=request, response=response)

    return _update_product
