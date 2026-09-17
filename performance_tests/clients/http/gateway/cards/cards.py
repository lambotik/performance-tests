from httpx import Response
from performance_tests.clients.http.client import HTTPClient, build_gateway_http_client

from performance_tests.clients.http.gateway.cards.schema import IssuePhysicalCardRequestSchema


class CardsGatewayHTTPClient(HTTPClient):

    def post_open_virtual_card_api(self, payload: dict) -> Response:
        """
        Выпуск виртуальной карты.
        :param payload: Словарь с данными для выпуска виртуальной карты.
        :return: Ответ от сервера (объект Response).
        """
        validated_request = IssuePhysicalCardRequestSchema(**payload)
        return self.post('/api/v1/cards/issue-virtual-card', json=validated_request.model_dump())

    def issue_physical_card_api(self, payload: dict) -> Response:
        """
        Выпуск физической карты.
        :param payload: Словарь с данными для выпуска физической карты.
        :return: Ответ от сервера (объект Response).
        """
        validated_request = IssuePhysicalCardRequestSchema(**payload)
        return self.post("/api/v1/cards/issue-physical-card", json=validated_request.model_dump())


def build_cards_gateway_http_client() -> CardsGatewayHTTPClient:
    """
    Функция создаёт экземпляр CardsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CardsGatewayHTTPClient.
    """
    return CardsGatewayHTTPClient(build_gateway_http_client())
