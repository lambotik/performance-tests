from performance_tests.clients.http.gateway.accounts.accounts_client import build_accounts_gateway_http_client, \
    AccountsGatewayHTTPClient
from performance_tests.clients.http.gateway.cards.cards_client import build_cards_gateway_http_client, CardsGatewayHTTPClient
from performance_tests.clients.http.gateway.documents.documents_client import DocumentsGatewayHTTPClient, \
    build_documents_gateway_http_client
from performance_tests.clients.http.gateway.operations.operations_client import OperationsGatewayHTTPClient, \
    build_operations_gateway_http_client
from performance_tests.clients.http.gateway.users.users_client import build_users_gateway_http_client, UsersGatewayHTTPClient


class TestHttpxApi:
    def test_open_deposit_account(self):
        users: UsersGatewayHTTPClient = build_users_gateway_http_client()
        accounts: AccountsGatewayHTTPClient = build_accounts_gateway_http_client()
        create_user_response = users.create_user()
        user_id = create_user_response.user.id
        open_deposit_account_response = accounts.open_deposit_account(user_id=user_id)
        response_get_deposits_accounts = accounts.get_accounts(user_id)
        accounts.open_credit_card_account(user_id=user_id)

    def test_create_virtual_card(self):
        users: UsersGatewayHTTPClient = build_users_gateway_http_client()
        cards: CardsGatewayHTTPClient = build_cards_gateway_http_client()
        accounts: AccountsGatewayHTTPClient = build_accounts_gateway_http_client()
        create_user_response = users.create_user()
        user_id = create_user_response.user.id
        print(type(user_id))
        open_debit_card_account_response = accounts.open_debit_card_account(user_id=user_id)
        account_id = open_debit_card_account_response.account.id
        print(type(account_id))
        create_virtual_card_response = cards.issue_virtual_card(user_id=user_id, account_id=account_id)
        print(create_virtual_card_response)

    def test_get_document(self):
        users: UsersGatewayHTTPClient = build_users_gateway_http_client()
        accounts: AccountsGatewayHTTPClient = build_accounts_gateway_http_client()
        documents: DocumentsGatewayHTTPClient = build_documents_gateway_http_client()
        create_user_response = users.create_user()
        user_id = create_user_response.user.id
        response_open_credit_card_account = accounts.open_credit_card_account(user_id)
        account_id = response_open_credit_card_account.account.id
        response_get_tariff = documents.get_tariff_document_api(account_id)
        assert response_get_tariff.status_code is 200
        response_get_contract_document = documents.get_contract_document_api(account_id)
        assert response_get_contract_document.status_code is 200

    def test_make_top_up_operation(self):
        users: UsersGatewayHTTPClient = build_users_gateway_http_client()
        accounts: AccountsGatewayHTTPClient = build_accounts_gateway_http_client()
        operations: OperationsGatewayHTTPClient = build_operations_gateway_http_client()
        create_user_response = users.create_user()
        user_id = create_user_response.user.id
        response_open_debit_card_account = accounts.open_debit_card_account(user_id=user_id)
        card_id = response_open_debit_card_account.account.cards[0].id
        account_id = response_open_debit_card_account.account.id
        print(type(user_id), type(account_id))
        operations.make_top_up_operation(card_id=card_id, account_id=account_id)

    def test_make_purchase_operation(self):
        users: UsersGatewayHTTPClient = build_users_gateway_http_client()
        accounts: AccountsGatewayHTTPClient = build_accounts_gateway_http_client()
        operations: OperationsGatewayHTTPClient = build_operations_gateway_http_client()
        create_user_response = users.create_user()
        user_id = create_user_response.user.id
        response_open_debit_card_account = accounts.open_debit_card_account(user_id=user_id)
        card_id = response_open_debit_card_account.account.cards[0].id
        account_id = response_open_debit_card_account.account.id
        response_make_purchase_operation = operations.make_purchase_operation(
            card_id=card_id,
            account_id=account_id)
        operation_id = response_make_purchase_operation.operation.id
        response_receipt_operation = operations.get_operation_receipt_api(operation_id=operation_id)
        assert response_receipt_operation.status_code is 200

    def test_client_get_documents(self):
        users: UsersGatewayHTTPClient = build_users_gateway_http_client()
        accounts: AccountsGatewayHTTPClient = build_accounts_gateway_http_client()
        documents: DocumentsGatewayHTTPClient = build_documents_gateway_http_client()
        create_user_response = users.create_user()
        print('Create user response:', create_user_response)

        open_credit_card_account_response = accounts.open_credit_card_account(user_id=create_user_response.user.id)
        print('Open credit card account response:', open_credit_card_account_response)

        get_tariff_document_response = documents.get_tariff_document_api(
            account_id=open_credit_card_account_response.account.id
        )
        print('Get tariff document response:', get_tariff_document_response.json())

        get_contract_document_response = documents.get_contract_document_api(
            account_id=open_credit_card_account_response.account.id
        )
        print('Get contract document response:', get_contract_document_response)

    def test_client_make_top_up_operation(self):
        users: UsersGatewayHTTPClient = build_users_gateway_http_client()
        accounts: AccountsGatewayHTTPClient = build_accounts_gateway_http_client()
        operations: OperationsGatewayHTTPClient = build_operations_gateway_http_client()
        create_user_response = users.create_user()
        print('Create user response:', create_user_response)
        open_debit_card_account_response = accounts.open_debit_card_account(
            user_id=create_user_response.user.id
        )
        print('Open debit card account response:', open_debit_card_account_response)
        card_id = open_debit_card_account_response.account.cards[0].id
        account_id = open_debit_card_account_response.account.id
        make_top_up_operation_response = operations.make_cashback_operation(card_id, account_id)
        print('Make top up operation response:', make_top_up_operation_response)
