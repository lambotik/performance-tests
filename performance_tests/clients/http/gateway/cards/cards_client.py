from uuid import UUID

from httpx import Response
from locust.env import Environment

from performance_tests.clients.http.client import HTTPClient, build_gateway_http_client, \
    build_gateway_locust_http_client

from performance_tests.clients.http.gateway.cards.schema import IssuePhysicalCardRequestSchema, \
    IssueVirtualCardRequestSchema
from services.gateway.apps.cards.schema.cards import IssueVirtualCardResponseSchema, IssuePhysicalCardResponseSchema


class CardsGatewayHTTPClient(HTTPClient):

    def issue_virtual_card_api(self, request: IssueVirtualCardRequestSchema) -> Response:
        """
        Выпуск виртуальной карты.

        :param request: Pydantic-модель с данными для выпуска виртуальной карты.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post(
            "/api/v1/cards/issue-virtual-card",
            json=request.model_dump(mode='json', by_alias=True)
        )
        # mode='json' гарантирует, что все UUID, datetime и т.д.
        # будут преобразованы в строки для безопасной сериализации в httpx

    def issue_physical_card_api(self, request: IssuePhysicalCardRequestSchema) -> Response:
        """
        Выпуск физической карты.

        :param request: Pydantic-модель с данными для выпуска физической карты.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post(
            "/api/v1/cards/issue-physical-card",
            json=request.model_dump(mode='json', by_alias=True)
        )


    def issue_virtual_card(self, user_id: str | UUID, account_id: UUID) -> IssueVirtualCardResponseSchema:
        request = IssueVirtualCardRequestSchema(user_id=user_id, account_id=account_id)
        response = self.issue_virtual_card_api(request)
        return IssueVirtualCardResponseSchema.model_validate_json(response.text)

    def issue_physical_card(self, user_id: str | UUID, account_id: str) -> IssuePhysicalCardResponseSchema:
        request = IssuePhysicalCardRequestSchema(user_id=user_id, account_id=account_id)
        response = self.issue_physical_card_api(request)
        return IssuePhysicalCardResponseSchema.model_validate_json(response.text)


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
