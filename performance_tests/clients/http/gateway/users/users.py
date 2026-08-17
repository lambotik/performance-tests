import httpx
from httpx import Response

from pydantic import BaseModel

from performance_tests.clients.http.client import HTTPClient



class CreateUserRequestDict(BaseModel):
    email: str
    lastName: str
    firstName: str
    middleName: str
    phoneNumber: str


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

    def post_create_user(self, payload: dict) -> Response:
        """
        Создание нового пользователя.
        :param payload: Словарь с данными нового пользователя.
        :return: Ответ от сервера (объект Response).
        """
        validated_request = CreateUserRequestDict(**payload)
        return self.post('/api/v1/users', json=validated_request.model_dump())
