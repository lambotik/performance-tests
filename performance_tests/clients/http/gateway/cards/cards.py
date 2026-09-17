from httpx import Response
from locust.env import Environment

from performance_tests.clients.http.client import HTTPClient, build_gateway_http_client, \
    build_gateway_locust_http_client

from performance_tests.clients.http.gateway.cards.schema import IssuePhysicalCardRequestSchema, \
    IssueVirtualCardRequestSchema


class CardsGatewayHTTPClient(HTTPClient):

    def post_open_virtual_card_api(self, user_id: str, account_id: str) -> Response:
        """
        Выпуск виртуальной карты.
        :param user_id
        :param account_id
        :return: Ответ от сервера (объект Response).
        """
        validated_request = IssueVirtualCardRequestSchema(user_id=user_id, account_id=account_id)
        return self.post('/api/v1/cards/issue-virtual-card', json=validated_request.model_dump(by_alias=True))

    def issue_physical_card_api(self, user_id: str, account_id: str) -> Response:
        """
        Выпуск физической карты.
        :param user_id
        :param account_id
        :return: Ответ от сервера (объект Response).
        """
        validated_request = IssuePhysicalCardRequestSchema(user_id=user_id, account_id=account_id)
        return self.post("/api/v1/cards/issue-physical-card", json=validated_request.model_dump(by_alias=True))


def build_cards_gateway_http_client() -> CardsGatewayHTTPClient:
    """
    Функция создаёт экземпляр CardsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CardsGatewayHTTPClient.
    """
    return CardsGatewayHTTPClient(client=build_gateway_http_client())


# Новый билдер для нагрузочного тестирования
def build_cards_gateway_locust_http_client(environment: Environment) -> CardsGatewayHTTPClient:
    """
    Функция создаёт экземпляр CardsGatewayHTTPClient адаптированного под Locust.

    Клиент автоматически собирает метрики и передаёт их в Locust через хуки.
    Используется исключительно в нагрузочных тестах.

    :param environment: объект окружения Locust.
    :return: экземпляр CardsGatewayHTTPClient с хуками сбора метрик.
    """
    return CardsGatewayHTTPClient(client=build_gateway_locust_http_client(environment))
