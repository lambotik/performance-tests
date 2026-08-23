import httpx
from httpx import Response, QueryParams
from pydantic import BaseModel

from performance_tests.clients.http.client import HTTPClient


class GetAccountsQueryDict(BaseModel):
    """
    Структура данных для получения списка счетов пользователя.
    """
    userId: str


class OpenDepositAccountRequestDict(BaseModel):
    """
    Структура данных для открытия депозитного счета.
    """
    userId: str


class OpenSavingsAccountRequestDict(BaseModel):
    """
    Структура данных для открытия сберегательного счета.
    """
    userId: str


class OpenDebitCardAccountRequestDict(BaseModel):
    """
    Структура данных для открытия дебетового счета.
    """
    userId: str


class OpenCreditCardAccountRequestDict(BaseModel):
    """
    Структура данных для открытия кредитного счета.
    """
    userId: str


class AccountsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/accounts сервиса http-gateway.
    """

    def __init__(self, base_url: str):
        super().__init__(base_url)
        if not base_url:
            raise ValueError("base_url обязателен!")
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client(base_url=self.base_url, timeout=5.0)

    def get_accounts_api(self, query: dict) -> Response:
        """
        Выполняет GET-запрос на получение списка счетов пользователя.
        :param query: Словарь с параметрами запроса, например: {'userId': '123'}.
        :return: Объект Response с данными о счетах.
        """
        validated_request = GetAccountsQueryDict(**query)
        return self.get(f"/api/v1/accounts", params=QueryParams(validated_request.model_dump()))

    def post_open_deposit_account(self, user_id: str) -> Response:
        """
        Выполняет POST-запрос для открытия депозитного счёта.
        :param user_id: 1722f0d4-576b-460e-ba51-6dbe1469f86e
        :return: Объект Response с результатом операции.
        """
        payload = OpenDepositAccountRequestDict(userId=user_id).model_dump()
        return self.post('/api/v1/accounts/open-deposit-account', json=payload)

    def open_savings_account_api(self, user_id: str) -> Response:
        """
        Выполняет POST-запрос для открытия сберегательного счёта.
        :param user_id:  1722f0d4-576b-460e-ba51-6dbe1469f86e
        :return: Объект Response.
        """
        payload = OpenSavingsAccountRequestDict(userId=user_id).model_dump()
        return self.post("/api/v1/accounts/open-savings-account", json=payload)

    def post_open_debit_card_account(self, user_id: str) -> Response:
        """
        Выполняет POST-запрос для открытия дебетовой карты.
        :param user_id:1722f0d4-576b-460e-ba51-6dbe1469f86e
        :return: Объект Response.
        """
        payload = OpenDebitCardAccountRequestDict(userId=user_id).model_dump()
        return self.post('/api/v1/accounts/open-debit-card-account', json=payload)

    def post_open_credit_card_account(self, user_id: str) -> httpx.Response:
        """
        Выполняет POST-запрос для открытия кредитной карты.
        :param user_id: 1722f0d4-576b-460e-ba51-6dbe1469f86e
        :return: Объект Response.
        """
        payload = OpenCreditCardAccountRequestDict(userId=user_id).model_dump()
        return self.post('/api/v1/accounts/open-credit-card-account', json=payload)
