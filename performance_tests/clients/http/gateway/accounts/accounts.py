import httpx
from httpx import Response

from performance_tests.clients.http.client import HTTPClient


class AccountsGatewayHTTPClient(HTTPClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        if not base_url:
            raise ValueError("base_url обязателен!")
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client(base_url=self.base_url, timeout=5.0)

    def post_open_deposit_account(self, user_id: str) -> Response:
        payload = {"userId": user_id}
        return self.post('/api/v1/accounts/open-deposit-account', json=payload)

    def post_open_debit_card_account(self, user_id: str) -> Response:
        payload = {"userId": user_id}
        return self.post('/api/v1/accounts/open-debit-card-account', json=payload)

    def post_open_credit_card_account(self, user_id: str) -> httpx.Response:
        payload = {"userId": user_id}
        return self.post('/api/v1/accounts/open-credit-card-account', json=payload)
