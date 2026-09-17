import httpx
from httpx import Response, QueryParams
from locust.env import Environment

from performance_tests.clients.http.client import (
    HTTPClient,
    HTTPClientExtensions,
    build_gateway_http_client,
    build_gateway_locust_http_client
)
from performance_tests.clients.http.gateway.accounts.schema import (
    GetAccountsQuerySchema,
    OpenDepositAccountRequestSchema,
    OpenSavingsAccountRequestSchema,
    OpenDebitCardAccountRequestSchema,
    OpenCreditCardAccountRequestSchema
)


class AccountsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/accounts сервиса http-gateway.
    """

    def get_accounts_api(self, query: GetAccountsQuerySchema):
        """
        Выполняет GET-запрос на получение списка счетов пользователя.

        :param query: Pydantic-модель с параметрами запроса, например: {'userId': '123'}.
        :return: Объект httpx.Response с данными о счетах.
        """
        return self.get(
            "/api/v1/accounts",
            params=QueryParams(**query.model_dump(by_alias=True)),
            extensions=HTTPClientExtensions(route="/api/v1/accounts")  # Явно передаём логическое имя маршрута
        )

    def post_open_deposit_account_api(self, user_id: str) -> Response:
        """
        Выполняет POST-запрос для открытия депозитного счёта.
        :param user_id: 1722f0d4-576b-460e-ba51-6dbe1469f86e
        :return: Объект Response с результатом операции.
        """
        payload = OpenDepositAccountRequestSchema(user_id=str(user_id)).model_dump()
        return self.post('/api/v1/accounts/open-deposit-account', json=payload)

    def open_savings_account_api(self, user_id: str) -> Response:
        """
        Выполняет POST-запрос для открытия сберегательного счёта.
        :param user_id:  1722f0d4-576b-460e-ba51-6dbe1469f86e
        :return: Объект Response.
        """
        payload = OpenSavingsAccountRequestSchema(user_id=user_id).model_dump()
        return self.post("/api/v1/accounts/open-savings-account", json=payload)

    def post_open_debit_card_account_api(self, user_id: str) -> Response:
        """
        Выполняет POST-запрос для открытия дебетовой карты.
        :param user_id:1722f0d4-576b-460e-ba51-6dbe1469f86e
        :return: Объект Response.
        """
        payload = OpenDebitCardAccountRequestSchema(user_id=user_id).model_dump()
        return self.post('/api/v1/accounts/open-debit-card-account', json=payload)

    def post_open_credit_card_account_api(self, user_id: str) -> httpx.Response:
        """
        Выполняет POST-запрос для открытия кредитной карты.
        :param user_id: 1722f0d4-576b-460e-ba51-6dbe1469f86e
        :return: Объект Response.
        """
        payload = OpenCreditCardAccountRequestSchema(user_id=user_id).model_dump()
        return self.post('/api/v1/accounts/open-credit-card-account', json=payload)


def build_accounts_gateway_http_client() -> AccountsGatewayHTTPClient:
    """
    Функция создаёт экземпляр AccountsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AccountsGatewayHTTPClient.
    """
    return AccountsGatewayHTTPClient(client=build_gateway_http_client())


# Новый билдер для нагрузочного тестирования
def build_accounts_gateway_locust_http_client(environment: Environment) -> AccountsGatewayHTTPClient:
    """
    Функция создаёт экземпляр AccountsGatewayHTTPClient адаптированного под Locust.

    Клиент автоматически собирает метрики и передаёт их в Locust через хуки.
    Используется исключительно в нагрузочных тестах.

    :param environment: объект окружения Locust.
    :return: экземпляр AccountsGatewayHTTPClient с хуками сбора метрик.
    """
    return AccountsGatewayHTTPClient(client=build_gateway_locust_http_client(environment))
