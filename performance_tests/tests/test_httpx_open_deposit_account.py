from performance_tests.clients.http.gateway.payload_data import DataPayload
from performance_tests.conftest import *


class TestHttpxApi:
    def test_open_deposit_account(self,
                                  users: UsersGatewayHTTPClient,
                                  accounts: AccountsGatewayHTTPClient):
        create_user_response = users.post_create_user_api(DataPayload.user_create_payload())
        create_user_response_data = create_user_response.json()
        user_id = create_user_response_data["user"]["id"]
        open_deposit_account_response = accounts.post_open_deposit_account_api(user_id=user_id)
        assert open_deposit_account_response.status_code is 200
        response_get_deposits_accounts = accounts.get_accounts_api({"userId": user_id})
        assert response_get_deposits_accounts.status_code is 200
        response_open_credit_account = accounts.post_open_credit_card_account_api(user_id=user_id)
        assert response_open_credit_account.status_code is 200

    def test_create_virtual_card(self,
                                 users: UsersGatewayHTTPClient,
                                 accounts: AccountsGatewayHTTPClient,
                                 cards: CardsGatewayHTTPClient):
        create_user_response = users.post_create_user_api(DataPayload.user_create_payload())
        assert create_user_response.status_code is 200, 'User is not created'
        create_user_response_data = create_user_response.json()
        user_id = create_user_response_data["user"]["id"]
        open_debit_card_account_response = accounts.post_open_debit_card_account_api(user_id=user_id)
        account_id = open_debit_card_account_response.json()["account"]["id"]
        assert open_debit_card_account_response.status_code is 200, 'Debit card is not created'
        create_virtual_card_response = cards.post_open_virtual_card_api(
            DataPayload.open_virtual_card_payload(user_id=user_id, account_id=account_id))
        assert create_virtual_card_response.status_code is 200, 'Virtual card is not created'

    def test_get_document(self,
                          users: UsersGatewayHTTPClient,
                          accounts: AccountsGatewayHTTPClient,
                          documents: DocumentsGatewayHTTPClient):
        create_user_response = users.post_create_user_api(DataPayload.user_create_payload())
        assert create_user_response.status_code is 200, 'User is not created'
        user_id = create_user_response.json()["user"]["id"]
        response_open_credit_card_account = accounts.post_open_credit_card_account_api(user_id)
        assert response_open_credit_card_account.status_code is 200
        account_id = response_open_credit_card_account.json()["account"]["id"]
        response_get_tariff = documents.get_tariff_document_api(account_id)
        assert response_get_tariff.status_code is 200
        response_get_contract_document = documents.get_contract_document_api(account_id)
        assert response_get_contract_document.status_code is 200

    def test_make_top_up_operation(self,
                                   users: UsersGatewayHTTPClient,
                                   accounts: AccountsGatewayHTTPClient,
                                   operations: OperationsGatewayHTTPClient):
        create_user_response = users.post_create_user_api(DataPayload.user_create_payload())
        assert create_user_response.status_code is 200, 'User is not created'
        user_id = create_user_response.json()["user"]["id"]
        response_open_debit_card_account = accounts.post_open_debit_card_account_api(user_id=user_id)
        card_id = response_open_debit_card_account.json()["account"]["cards"][0]["id"]
        account_id = response_open_debit_card_account.json()["account"]["id"]
        operations.make_top_up_operation(card_id=card_id, account_id=account_id)

    def test_make_purchase_operation(self,
                                     users: UsersGatewayHTTPClient,
                                     accounts: AccountsGatewayHTTPClient,
                                     operations: OperationsGatewayHTTPClient):
        create_user_response = users.post_create_user_api(DataPayload.user_create_payload())
        assert create_user_response.status_code is 200, 'User is not created'
        user_id = create_user_response.json()["user"]["id"]
        response_open_debit_card_account = accounts.post_open_debit_card_account_api(user_id=user_id)
        card_id = response_open_debit_card_account.json()["account"]["cards"][0]["id"]
        account_id = response_open_debit_card_account.json()["account"]["id"]
        response_make_purchase_operation = operations.make_purchase_operation(
            card_id=card_id,
            account_id=account_id)
        operation_id = response_make_purchase_operation.operation.id
        response_receipt_operation = operations.get_operation_receipt_api(operation_id=operation_id)
        assert response_receipt_operation.status_code is 200

    def test_client_get_documents(self,
                                  users: UsersGatewayHTTPClient,
                                  accounts: AccountsGatewayHTTPClient,
                                  documents: DocumentsGatewayHTTPClient):
        create_user_response = users.create_user()
        print('Create user response:', create_user_response)
        assert create_user_response['user'] != {}

        open_credit_card_account_response = accounts.post_open_credit_card_account_api(
            user_id=create_user_response['user']['id']
        )
        assert str(open_credit_card_account_response) == '<Response [200 OK]>'
        print('Open credit card account response:', open_credit_card_account_response.json())

        get_tariff_document_response = documents.get_tariff_document_api(
            account_id=open_credit_card_account_response.json()['account']['id']
        )
        assert str(get_tariff_document_response) == '<Response [200 OK]>'
        print('Get tariff document response:', get_tariff_document_response.json())

        get_contract_document_response = documents.get_contract_document_api(
            account_id=open_credit_card_account_response.json()['account']['id']
        )
        assert str(get_contract_document_response) == '<Response [200 OK]>'
        print('Get contract document response:', get_contract_document_response)

    def test_client_make_top_up_operation(self, users: UsersGatewayHTTPClient,
                                          accounts: AccountsGatewayHTTPClient,
                                          operations: OperationsGatewayHTTPClient):
        create_user_response = users.create_user()
        print('Create user response:', create_user_response)
        open_debit_card_account_response = accounts.post_open_debit_card_account_api(
            user_id=create_user_response['user']['id']
        )
        print('Open debit card account response:', open_debit_card_account_response)
        card_id = open_debit_card_account_response.json()['account']['cards'][0]['id']
        account_id = open_debit_card_account_response.json()['account']['id']
        make_top_up_operation_response = operations.make_cashback_operation(card_id, account_id)
        print('Make top up operation response:', make_top_up_operation_response)
