import time

from httpx import Response
from locust.env import Environment

from performance_tests.clients.http.client import (
    HTTPClient,
    HTTPClientExtensions,
    build_gateway_http_client,
    build_gateway_locust_http_client
)
from performance_tests.clients.http.gateway.users.schema import CreateUserResponseSchema, CreateUserRequestSchema, User
from services.users.apps.users.schema.users import GetUserResponseSchema


class UsersGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/users сервиса http-gateway.
    """

    def get_user_api(self, user_id: str) -> Response:
        """
        Получить данные пользователя по его user_id.

        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера (объект httpx.Response).
        """

        return self.get(
            f"/api/v1/users/{user_id}",
            extensions=HTTPClientExtensions(route="/api/v1/users/{user_id}")  # Явно передаём логическое имя маршрута
        )

    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """
        Создание нового пользователя.

        :param request: Словарь с данными нового пользователя.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/users", json=request.model_dump())

    def get_user(self, user_id: str) -> GetUserResponseSchema:
        response = self.get_user_api(user_id)
        return response.json()

    def create_user(self) -> CreateUserResponseSchema:
        # Генерация данных теперь происходит внутри схемы запроса
        request = CreateUserRequestSchema()
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)


def build_users_gateway_http_client() -> UsersGatewayHTTPClient:
    """
    Функция создаёт экземпляр UsersGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию UsersGatewayHTTPClient.
    """
    return UsersGatewayHTTPClient(client=build_gateway_http_client())


# Новый билдер для нагрузочного тестирования
def build_users_gateway_locust_http_client(environment: Environment) -> UsersGatewayHTTPClient:
    """
    Функция создаёт экземпляр UsersGatewayHTTPClient адаптированного под Locust.

    Клиент автоматически собирает метрики и передаёт их в Locust через хуки.
    Используется исключительно в нагрузочных тестах.

    :param environment: объект окружения Locust.
    :return: экземпляр UsersGatewayHTTPClient с хуками сбора метрик.
    """
    return UsersGatewayHTTPClient(client=build_gateway_locust_http_client(environment))
