#client.py
from typing import Optional, Dict, Any

import httpx
from httpx import URL, QueryParams, Response


class HTTPClient:
    def __init__(self, base_url: str = None, headers: Dict = None):
        self.base_url = base_url
        self.client = httpx.Client(
            base_url=base_url,
            headers=headers or {},
            timeout=30.0
        )

    def request(self, method: str, endpoint: URL | str, **kwargs) -> Response:
        """
        :param method:
        :param endpoint:
        :param kwargs:
        :return:
        """
        return self.client.request(method, endpoint, **kwargs)

    def get(self, endpoint: URL | str, params: QueryParams | None = None) -> Response:
        """
        Выполняет GET-запрос.
        :param endpoint: URL-адрес эндпоинта.
        :param params: GET-параметры запроса (например, ?key=value).
        :return: Объект Response с данными ответа.
        """
        return self.client.get(endpoint, params=params)

    def post(self, endpoint: URL | str, json: Any | None = None) -> Response:
        """
        Выполняет POST-запрос.
        :param endpoint: URL-адрес эндпоинта.
        :param json: Данные в формате JSON.
        :return: Объект Response с данными ответа.
        """
        return self.client.post(endpoint, json=json)

    def close(self):
        if hasattr(self, 'client'):
            self.client.close()
