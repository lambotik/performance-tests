import os
import pytest

from performance_tests.clients.http.gateway.accounts.accounts import AccountsGatewayHTTPClient
from performance_tests.clients.http.gateway.cards.cards import CardsGatewayHTTPClient
from performance_tests.clients.http.gateway.documents.documents import DocumentsGatewayHTTPClient
from performance_tests.clients.http.gateway.operations.operations import OperationsGatewayHTTPClient
from performance_tests.clients.http.gateway.users.users import UsersGatewayHTTPClient


@pytest.fixture
def api_client_factory():
    """Фабрика для создания API клиентов"""
    base_url = os.getenv("API_BASE_URL", "http://localhost:8003")

    def create_client(client_type: str):
        clients = {
            "users": UsersGatewayHTTPClient,
            "accounts": AccountsGatewayHTTPClient,
            "cards": CardsGatewayHTTPClient,
            "documents": DocumentsGatewayHTTPClient,
            "operations": OperationsGatewayHTTPClient,
            # добавьте другие клиенты
        }
        if client_type not in clients:
            raise ValueError(f"Unknown client type: {client_type}")
        return clients[client_type](base_url=base_url)

    yield create_client


@pytest.fixture
def users(api_client_factory):
    """Фикстура для клиента пользователей"""
    client = api_client_factory("users")
    yield client
    client.close()


@pytest.fixture
def accounts(api_client_factory):
    """Фикстура для клиента аккаунтов"""
    client = api_client_factory("accounts")
    yield client
    client.close()

@pytest.fixture
def cards(api_client_factory):
    """Фикстура для клиента карт"""
    client = api_client_factory("cards")
    yield client
    client.close()


@pytest.fixture
def documents(api_client_factory):
    """Фикстура для клиента документов"""
    client = api_client_factory("documents")
    yield client
    client.close()

@pytest.fixture
def operations(api_client_factory):
    """Фикстура для клиента операций"""
    client = api_client_factory("operations")
    yield client
    client.close()