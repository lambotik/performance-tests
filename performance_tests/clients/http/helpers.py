import uuid
import httpx
from typing_extensions import TypedDict


class CreateUserRequestDict(TypedDict):
    email: str
    lastName: str
    firstName: str
    middleName: str
    phoneNumber: str


class MakePurchaseRequestDict(TypedDict):
    status: str
    amount: int | float
    cardId: str
    accountId: str
    category: str


class HTTPClientHelpers:
    def __init__(self, base_url: str):
        if not base_url:
            raise ValueError("base_url обязателен!")
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client(base_url=self.base_url, timeout=5.0)

    def post(self, endpoint: str, **kwargs) -> httpx.Response:
        return self.client.post(endpoint, **kwargs)

    def get(self, endpoint: str, **kwargs) -> httpx.Response:
        return self.client.get(endpoint, **kwargs)

    def close(self):
        if hasattr(self, 'client'):
            self.client.close()

    def post_create_user(self) -> httpx.Response:
        payload = {
            "email": f"user.{uuid.uuid4()}@example.com",
            "lastName": "string",
            "firstName": "string",
            "middleName": "string",
            "phoneNumber": "string"
        }
        return self.post('/api/v1/users', json=payload)

    def post_open_deposit_account(self, user_id: str) -> httpx.Response:
        payload = {"userId": user_id}
        return self.post('/api/v1/accounts/open-deposit-account', json=payload)

    def post_open_debit_card_account(self, user_id: str) -> httpx.Response:
        payload = {"userId": user_id}
        return self.post('/api/v1/accounts/open-debit-card-account', json=payload)

    def post_open_virtual_card(self, user_id: str, account_id: str) -> httpx.Response:
        payload = {"userId": user_id, "accountId": account_id}
        return self.post('/api/v1/cards/issue-virtual-card', json=payload)

    def post_open_credit_card_account(self, user_id: str) -> httpx.Response:
        payload = {"userId": user_id}
        return self.post('/api/v1/accounts/open-credit-card-account', json=payload)

    def get_tariff_document(self, account_id: str) -> httpx.Response:
        return self.get(f'/api/v1/documents/tariff-document/{account_id}')

    def get_contract_document(self, account_id: str) -> httpx.Response:
        return self.get(f'/api/v1/documents/contract-document/{account_id}')

    def post_make_top_up_operation(self, account_id: str, card_id: str) -> httpx.Response:
        payload = {
            "status": "COMPLETED",
            "amount": 1500,
            "cardId": card_id,
            "accountId": account_id
        }
        return self.post('/api/v1/operations/make-top-up-operation', json=payload)

    def post_make_purchase_operation(self, account_id: str, card_id: str, status: str, amount: int | float, category: str) -> httpx.Response:
        payload = {
            "status": status,
            "amount": amount,
            "cardId": card_id,
            "accountId": account_id,
            "category": category
        }
        return self.post('/api/v1/operations/make-purchase-operation', json=payload)

    def get_operation_receipt(self, operation_id: str) -> httpx.Response:
        return self.get(f'/api/v1/operations/operation-receipt/{operation_id}')