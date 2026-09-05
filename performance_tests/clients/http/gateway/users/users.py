import os

import httpx
from httpx import Response
from dotenv import load_dotenv

from performance_tests.clients.http.client import HTTPClient
from performance_tests.clients.http.gateway.models import DataPayload, CreateUserRequestDict, CreateUserResponseSchema

load_dotenv()


class UsersGatewayHTTPClient(HTTPClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        if not base_url:
            raise ValueError("base_url обязателен!")
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client(base_url=self.base_url, timeout=5.0)

    def get_user_api(self, user_id: str) -> Response:
        """
        Получить данные пользователя по его user_id.
        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера (объект Response).
        """
        return self.get(f"/api/v1/users/{user_id}")

    def post_create_user_api(self, payload: dict) -> Response:
        """
        Создание нового пользователя.
        :param payload: Словарь с данными нового пользователя.
        :return: Ответ от сервера (объект Response).
        """
        validated_request = CreateUserRequestDict(**payload)
        return self.post('/api/v1/users', json=validated_request.model_dump())

    def create_user(self) -> CreateUserResponseSchema:
        response = self.post_create_user_api(DataPayload.user_create_payload())
        if response.status_code != 200:  # или 200, в зависимости от API
            raise ValueError(f"API returned error: {response.status_code} - {response.text}")
        return response.json()


def build_users_gateway_http_client() -> UsersGatewayHTTPClient:
    """
    Функция создаёт экземпляр UsersGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию UsersGatewayHTTPClient.
    """
    return UsersGatewayHTTPClient(base_url=os.getenv("LOCAL_GATEWAY_HTTP_CLIENT.HOST"))
