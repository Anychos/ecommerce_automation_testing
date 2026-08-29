from typing import Any

import allure
from httpx import Client, URL, Response


class BaseAPIClient:
    """Базовый API клиент"""
    def __init__(self, client: Client):
        self.client = client

    def close(self) -> None:
        """Закрывает HTTP клиент"""
        self.client.close()

    @allure.step("Отправка GET запроса на {url}")
    def get(self,
            *,
            url: str | URL,
            params: str | None = None,
            headers: dict[str, str] | None = None
            ) -> Response:
        """
        Отправляет GET запрос

        :param url: URL ресурса
        :param params: Параметры запроса
        :param headers: Заголовки запроса
        :return: Ответ сервера
        """
        return self.client.get(url=url, params=params, headers=headers)

    @allure.step("Отправка POST запроса на {url}")
    def post(self,
             *,
             url: str | URL,
             json: Any,
             params: str | None = None,
             headers: dict[str, str] | None = None
             ) -> Response:
        """
        Отправляет POST запрос

        :param url: URL ресурса
        :param json: Данные запроса в формате JSON
        :param params: Параметры запроса
        :param headers: Заголовки запроса
        :return: Ответ сервера
        """
        return self.client.post(url=url, json=json, params=params, headers=headers)

    @allure.step("Отправка PUT запроса на {url}")
    def put(self,
            *,
            url: str | URL,
            json: Any,
            params: str | None = None,
            headers: dict[str, str] | None = None
            ) -> Response:
        """
        Отправляет PUT запрос

        :param url: URL ресурса
        :param json: Данные запроса в формате JSON
        :param params: Параметры запроса
        :param headers: Заголовки запроса
        :return: Ответ сервера
        """
        return self.client.put(url=url, json=json, params=params, headers=headers)

    @allure.step("Отправка PATCH запроса на {url}")
    def patch(self,
            *,
            url: str | URL,
            json: Any,
            params: str | None = None,
            headers: dict[str, str] | None = None
            ) -> Response:
        """
        Отправляет PATCH запрос

        :param url: URL ресурса
        :param json: Данные запроса в формате JSON
        :param params: Параметры запроса
        :param headers: Заголовки запроса
        :return: Ответ сервера
        """
        return self.client.patch(url=url, json=json, params=params, headers=headers)

    @allure.step("Отправка DELETE запроса на {url}")
    def delete(self,
               *,
               url: str | URL,
               params: str | None = None,
               headers: dict[str, str] | None = None
               ) -> Response:
        """
        Отправляет DELETE запрос

        :param url: URL ресурса
        :param params: Параметры запроса
        :param headers: Заголовки запроса
        :return: Ответ сервера
        """
        return self.client.delete(url=url, params=params, headers=headers)
