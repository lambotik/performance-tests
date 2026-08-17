import httpx
from httpx import Response
from pydantic import BaseModel

from performance_tests.clients.http.client import HTTPClient


class MakePurchaseRequestDict(BaseModel):
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


    def post_make_top_up_operation(self, payload: dict) -> Response:
        validated_request = MakeTopUpOperationRequestDict(**payload)
        return self.post('/api/v1/operations/make-top-up-operation', json=validated_request.model_dump())

    def post_make_purchase_operation(self, payload: dict) -> Response:
        validated_request = MakePurchaseRequestDict(**payload)
        return self.post('/api/v1/operations/make-purchase-operation', json=validated_request.model_dump())

    def get_receipt_operation(self, operation_id: str) -> Response:
        return self.get(f'/api/v1/operations/operation-receipt/{operation_id}')