import os
import time
from typing import Optional, Dict

import httpx
import pytest


class APIClient:
    """Универсальный клиент для работы с API."""

    _instance: Optional['APIClient'] = None

    def __new__(cls, base_url: Optional[str] = None, headers: Optional[Dict] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(base_url, headers)
        return cls._instance

    def _initialize(self, base_url: Optional[str] = None, headers: Optional[Dict] = None):
        self.base_url = base_url
        self.client = httpx.Client(
            base_url=base_url,
            headers=headers or {},
            timeout=30.0
        )

    def request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        return self.client.request(method, endpoint, **kwargs)

    def get(self, endpoint: str, **kwargs) -> httpx.Response:
        return self.client.get(endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> httpx.Response:
        return self.client.post(endpoint, **kwargs)

    def close(self):
        if hasattr(self, 'client'):
            self.client.close()


class Data:
    create_user_payload = {
        "email": f"user.{time.time()}@example.com",
        "lastName": "string",
        "firstName": "string",
        "middleName": "string",
        "phoneNumber": "string"
    }


class ApiHelpers(APIClient):
    def __init__(self, base_url: Optional[str] = None):
        if base_url is None:
            raise ValueError("base_url обязателен для создания клиента!")

        self.base_url = base_url.rstrip('/')  # Убираем лишний слэш в конце
        self.client = httpx.Client(
            base_url=self.base_url,  # httpx сам добавляет base_url к относительным путям!
            timeout=30.0
        )

    def post_create_user(self):
        return self.post(self.base_url + '/api/v1/users', json=Data.create_user_payload)

    def post_open_deposit_account(self, payload: Dict):
        """x
        {"userId": int}
        """
        return self.post(self.base_url + '/api/v1/accounts/open-deposit-account', json=payload)

@pytest.fixture
def api_helper():
    """Фикстура создаёт экземпляр ApiHelpers."""
    base_url = os.getenv("API_BASE_URL", 'http://localhost:8003')
    api = ApiHelpers(base_url=base_url)
    yield api
    api.close()


class TestHttpxApi:
    def test_open_deposit_account(self, api_helper: ApiHelpers):
        create_user_response = api_helper.post_create_user()
        create_user_response_data = create_user_response.json()
        open_deposit_account_payload = {"userId": create_user_response_data["user"]["id"]}
        open_deposit_account_response = api_helper.post_open_deposit_account(open_deposit_account_payload)
        print("Open deposit account response:", open_deposit_account_response.json())
        assert open_deposit_account_response.status_code is 200
