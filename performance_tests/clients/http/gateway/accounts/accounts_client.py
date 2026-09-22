from uuid import UUID

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
from services.gateway.apps.accounts.schema.accounts import OpenDebitCardAccountResponseSchema, \
    GetAccountsResponseSchema, OpenDepositAccountResponseSchema, OpenSavingsAccountResponseSchema, \
    OpenCreditCardAccountResponseSchema


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
            params=QueryParams(**query.model_dump(mode='json', by_alias=True)),
            extensions=HTTPClientExtensions(route="/api/v1/accounts")  # Явно передаём логическое имя маршрута
        )

    def open_deposit_account_api(self, request: OpenDepositAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия депозитного счёта.

        :param request: Pydantic-модель с userId.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(
            "/api/v1/accounts/open-deposit-account",
            json=request.model_dump(mode='json',
                                    by_alias=True))
        # mode='json' гарантирует, что все UUID, datetime и т.д.
        # будут преобразованы в строки для безопасной сериализации в httpx

    def open_savings_account_api(self, request: OpenSavingsAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия сберегательного счёта.

        :param request: Pydantic-модель с userId.
        :return: Объект httpx.Response.
        """
        return self.post(
            "/api/v1/accounts/open-savings-account",
            json=request.model_dump(mode='json', by_alias=True)
        )
        # mode='json' гарантирует, что все UUID, datetime и т.д.
        # будут преобразованы в строки для безопасной сериализации в httpx

    def open_debit_card_account_api(self, request: OpenDebitCardAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия дебетовой карты.

        :param request: Pydantic-модель с userId.
        :return: Объект httpx.Response.
        """
        return self.post(
            "/api/v1/accounts/open-debit-card-account",
            json=request.model_dump(mode='json', by_alias=True)
        )

    def open_credit_card_account_api(self, request: OpenCreditCardAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия кредитной карты.

        :param request: Pydantic-модель с userId.
        :return: Объект httpx.Response.
        """
        return self.post(
            "/api/v1/accounts/open-credit-card-account",
            json=request.model_dump(mode='json', by_alias=True)
        )

    def get_accounts(self, user_id: str | UUID) -> GetAccountsResponseSchema:
        query = GetAccountsQuerySchema(user_id=user_id)
        response = self.get_accounts_api(query)
        return GetAccountsResponseSchema.model_validate_json(response.text)

    def open_deposit_account(self, user_id: str | UUID) -> OpenDepositAccountResponseSchema:
        request = OpenDepositAccountRequestSchema(user_id=user_id)
        response = self.open_deposit_account_api(request)
        return OpenDepositAccountResponseSchema.model_validate_json(response.text)

    def open_savings_account(self, user_id: str | UUID) -> OpenSavingsAccountResponseSchema:
        request = OpenSavingsAccountRequestSchema(user_id=user_id)
        response = self.open_savings_account_api(request)
        return OpenSavingsAccountResponseSchema.model_validate_json(response.text)

    def open_debit_card_account(self, user_id: str | UUID) -> OpenDebitCardAccountResponseSchema:
        request = OpenDebitCardAccountRequestSchema(user_id=user_id)
        response = self.open_debit_card_account_api(request)
        return OpenDebitCardAccountResponseSchema.model_validate_json(response.text)

    def open_credit_card_account(self, user_id: str | UUID) -> OpenCreditCardAccountResponseSchema:
        request = OpenCreditCardAccountRequestSchema(user_id=user_id)
        response = self.open_credit_card_account_api(request)
        return OpenCreditCardAccountResponseSchema.model_validate_json(response.text)


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
