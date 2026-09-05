import os

import httpx
from httpx import Response
from performance_tests.clients.http.client import HTTPClient
from performance_tests.clients.http.gateway.models import IssuePhysicalCardRequestDict
from dotenv import load_dotenv

load_dotenv()


class CardsGatewayHTTPClient(HTTPClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        if not base_url:
            raise ValueError("base_url обязателен!")
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client(base_url=self.base_url, timeout=5.0)

    def post_open_virtual_card_api(self, payload: dict) -> Response:
        """
        Выпуск виртуальной карты.
        :param payload: Словарь с данными для выпуска виртуальной карты.
        :return: Ответ от сервера (объект Response).
        """
        validated_request = IssuePhysicalCardRequestDict(**payload)
        return self.post('/api/v1/cards/issue-virtual-card', json=validated_request.model_dump())

    def issue_physical_card_api(self, payload: dict) -> Response:
        """
        Выпуск физической карты.
        :param payload: Словарь с данными для выпуска физической карты.
        :return: Ответ от сервера (объект Response).
        """
        validated_request = IssuePhysicalCardRequestDict(**payload)
        return self.post("/api/v1/cards/issue-physical-card", json=validated_request.model_dump())


def build_cards_gateway_http_client() -> CardsGatewayHTTPClient:
    """
    Функция создаёт экземпляр CardsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CardsGatewayHTTPClient.
    """
    return CardsGatewayHTTPClient(base_url=os.getenv("LOCAL_GATEWAY_HTTP_CLIENT.HOST"))
