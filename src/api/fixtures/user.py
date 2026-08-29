from typing import Callable, Any, Generator

import pytest
from pydantic import BaseModel

from src.api.clients.authentication.schemas import LoginRequestSchema
from src.api.clients.user.client import UserAPIClient, get_private_admin_client, \
    get_private_user_client
from src.api.clients.user.schemas import CreateUserRequestSchema, CreateUserResponseSchema


class UserFixture(BaseModel):
    """Хранит данные о созданном пользователе"""
    request: CreateUserRequestSchema
    response: CreateUserResponseSchema

    @property
    def user_id(self) -> int:
        return self.response.id

    @property
    def email(self) -> str:
        return self.request.email

    @property
    def password(self) -> str:
        return self.request.password

    @property
    def user_schema(self) -> LoginRequestSchema:
        schema = LoginRequestSchema(
            email=self.request.email,
            password=self.request.password
        )
        return schema


@pytest.fixture
def private_admin_client() -> Generator[UserAPIClient, None, None]:
    """Возвращает готовый HTTP клиент для доступа администратора к приватному API пользователя"""
    client = get_private_admin_client()

    try:
        yield client
    finally:
        client.close()

@pytest.fixture
def create_user_factory(private_admin_client: UserAPIClient) -> Generator[Callable[..., UserFixture], None, None]:
    """
    Возвращает фабрику для создания пользователя

    :param private_admin_client: Приватный HTTP клиент для доступа администратора к API пользователя
    """
    created_users: list[UserFixture] = []

    def _create_user(
            *,
            is_admin: bool = False
    ) -> UserFixture:
        """
        Создает пользователя с указанными параметрами

        :param is_admin: Флаг администратора
        :return: Объект UserFixture с информацией о пользователе
        """
        request = CreateUserRequestSchema(is_admin=is_admin)

        response = private_admin_client.create_user(request=request)
        user = UserFixture(request=request, response=response)
        created_users.append(user)
        return user

    yield _create_user

    for user in created_users:
        private_admin_client.delete_user_api(user_id=user.user_id)

@pytest.fixture
def user(create_user_factory: Callable[..., UserFixture]) -> UserFixture:
    """
    Возвращает готового пользователя

    :param create_user_factory: Фабрика для создания пользователя
    :return: Объект UserFixture с информацией о пользователе
    """
    return create_user_factory()

@pytest.fixture
def private_user_client(user: UserFixture) -> Generator[UserAPIClient, None, None]:
    """
    Возвращает готовый HTTP клиент для доступа пользователя к приватному API пользователя

    :param user: Созданный пользователь
    """
    client = get_private_user_client(user=user.user_schema)

    try:
        yield client
    finally:
        client.close()

@pytest.fixture
def admin(create_user_factory: Callable[..., UserFixture]) -> UserFixture:
    """
    Возвращает готового администратора

    :param create_user_factory: Фабрика для создания пользователя
    :return: Объект UserFixture с информацией об администраторе
    """
    return create_user_factory(is_admin=True)



