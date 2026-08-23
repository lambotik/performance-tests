import httpx
from httpx import Response
from pydantic import BaseModel

from performance_tests.clients.http.client import HTTPClient


class MakePurchaseOperationRequestDict(BaseModel):
    status: str
    amount: int | float
    cardId: str
    accountId: str
    category: str


class MakeTopUpOperationRequestDict(BaseModel):
    status: str
    amount: int | float
    cardId: str
    accountId: str


class OperationsGatewayHTTPClient(HTTPClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        if not base_url:
            raise ValueError("base_url обязателен!")
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client(base_url=self.base_url, timeout=5.0)

    def get_operation_api(self, operation_id: str) -> Response:
        """
        Получает информацию об операции по её идентификатору.
        :param operation_id: Уникальный идентификатор операции.
        :return: Объект Response с данными об операции.
        """
        return self.get(f"/api/v1/operations/{operation_id}")

    def get_operation_receipt_api(self, operation_id: str) -> Response:
        """
        Получает чек по заданной операции.
        :param operation_id: Уникальный идентификатор операции.
        :return: Объект Response с чеком по операции.
        """
        return self.get(f"/api/v1/operations/operation-receipt/{operation_id}")

    def get_operations_api(self, account_id: str) -> Response:
        """
        Получает список операций по счёту.
        :param account_id: Словарь с параметром accountId.
        :return: Объект Response с операциями по счёту.
        """
        return self.get(f"/api/v1/operations/{account_id}")

    def get_operations_summary_api(self, account_id) -> Response:
        """
        Получает сводную статистику операций по счёту.
        :param account_id: Словарь с параметром accountId.
        :return: Объект Response с агрегированной информацией.
        """
        return self.get(f"/api/v1/operations/operations-summary/{account_id}")

    def make_fee_operation_api(self, payload: dict) -> Response:
        """
        Создаёт операцию комиссии.
        :param payload: Тело запроса с параметрами операции.
        :return: Объект Response с результатом операции.
        """
        return self.post("/api/v1/operations/make-fee-operation", json=payload)

    def make_top_up_operation_api(self, payload: dict) -> Response:
        """
        Создаёт операцию пополнения счёта.
        :param payload: Тело запроса с параметрами операции.
        :return: Объект Response с результатом операции.
        """
        validated_request = MakeTopUpOperationRequestDict(**payload)
        return self.post("/api/v1/operations/make-top-up-operation", json=validated_request.model_dump())

    def make_cashback_operation_api(self, payload: dict) -> Response:
        """
        Создаёт операцию начисления кэшбэка.
        :param payload: Тело запроса с параметрами операции.
        :return: Объект Response с результатом операции.
        """
        return self.post("/api/v1/operations/make-cashback-operation", json=payload)

    def make_transfer_operation_api(self, payload: dict) -> Response:
        """
        Создаёт операцию перевода средств.
        :param payload: Тело запроса с параметрами операции.
        :return: Объект Response с результатом операции.
        """
        return self.post("/api/v1/operations/make-transfer-operation", json=payload)

    def make_purchase_operation_api(self, payload: dict) -> Response:
        """
        Создаёт операцию покупки.
        :param payload: Тело запроса с параметрами операции, включая категорию.
        :return: Объект Response с результатом операции.
        """
        validated_request = MakePurchaseOperationRequestDict(**payload)
        return self.post("/api/v1/operations/make-purchase-operation", json=validated_request.model_dump())

    def make_bill_payment_operation_api(self, payload: dict) -> Response:
        """
        Создаёт операцию оплаты счёта.
        :param payload: Тело запроса с параметрами операции.
        :return: Объект Response с результатом операции.
        """
        return self.post("/api/v1/operations/make-bill-payment-operation", json=payload)

    def make_cash_withdrawal_operation_api(self, payload: dict) -> Response:
        """
        Создаёт операцию снятия наличных средств.
        :param payload: Тело запроса с параметрами операции.
        :return: Объект Response с результатом операции.
        """
        return self.post("/api/v1/operations/make-cash-withdrawal-operation", json=payload)
