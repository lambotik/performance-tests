import os

import httpx
from httpx import Response
from dotenv import load_dotenv

from performance_tests.clients.http.client import HTTPClient

load_dotenv()


class DocumentsGatewayHTTPClient(HTTPClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        if not base_url:
            raise ValueError("base_url обязателен!")
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client(base_url=self.base_url, timeout=5.0)

    def get_tariff_document_api(self, account_id: str) -> Response:
        """
        Получить тарифа по счету.
        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект Response).
        """
        return self.get(f"/api/v1/documents/tariff-document/{account_id}")

    def get_contract_document_api(self, account_id: str) -> Response:
        """
        Получить контракта по счету.
        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект Response).
        """
        return self.get(f"/api/v1/documents/contract-document/{account_id}")


def build_documents_gateway_http_client() -> DocumentsGatewayHTTPClient:
    """
    Функция создаёт экземпляр DocumentsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию DocumentsGatewayHTTPClient.
    """
    return DocumentsGatewayHTTPClient(base_url=os.getenv("LOCAL_GATEWAY_HTTP_CLIENT.HOST"))
