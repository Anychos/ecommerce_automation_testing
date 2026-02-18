import pytest

from src.ui.models.user_data import UserData
from src.ui.tools.data_generator import fake_ru


@pytest.fixture
def user_data_function() -> UserData:
    """
    Возвращает тестовые данные пользователя в пределах функции
    """

    password = fake_ru.password()
    data = UserData(
        email=fake_ru.email(),
        name=fake_ru.first_name(),
        phone=fake_ru.phone_number(),
        password=password,
        confirm_password=password
    )
    return data

@pytest.fixture(scope="session")
def user_data_session() -> UserData:
    """
    Возвращает тестовые данные пользователя в пределах сессии
    """

    password = fake_ru.password()
    data = UserData(
        email=fake_ru.email(),
        name=fake_ru.first_name(),
        phone=fake_ru.phone_number(),
        password=password,
        confirm_password=password
    )
    return data
