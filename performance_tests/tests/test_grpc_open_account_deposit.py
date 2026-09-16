from performance_tests.clients.grpc.gateway.accounts.client import build_accounts_gateway_grpc_client
from performance_tests.clients.grpc.gateway.documents.client import build_documents_gateway_grpc_client
from performance_tests.clients.grpc.gateway.operations.client import build_operations_gateway_grpc_client
from performance_tests.clients.grpc.gateway.users.client import build_users_gateway_grpc_client


class TestGRPCApi:
    def test_open_deposit_account(self):
        users = build_users_gateway_grpc_client()
        accounts = build_accounts_gateway_grpc_client()
        create_user_response = users.create_user()
        user_id = create_user_response.user.id
        open_deposit_account_response = accounts.open_deposit_account(user_id=user_id)
        print(open_deposit_account_response.account.status)
        assert open_deposit_account_response.account.status is 1

    def test_grpc_api_client_get_documents(self):
        users_gateway_client = build_users_gateway_grpc_client()
        accounts_gateway_client = build_accounts_gateway_grpc_client()
        documents_gateway_client = build_documents_gateway_grpc_client()

        create_user_response = users_gateway_client.create_user()
        print('Create user response:', create_user_response)

        open_credit_card_account_response = accounts_gateway_client.open_credit_card_account(
            user_id=create_user_response.user.id
        )
        print('Open credit card account response:', open_credit_card_account_response)

        get_tariff_document_response = documents_gateway_client.get_tariff_document(
            account_id=open_credit_card_account_response.account.id
        )
        print('Get tariff document response:', get_tariff_document_response)

        get_contract_document_response = documents_gateway_client.get_contract_document(
            account_id=open_credit_card_account_response.account.id
        )
        print('Get contract document response:', get_contract_document_response)

    def test_grpc_api_client_make_top_up_operation(self):
        users_gateway_client = build_users_gateway_grpc_client()
        accounts_gateway_client = build_accounts_gateway_grpc_client()
        operations_gateway_client = build_operations_gateway_grpc_client()

        create_user_response = users_gateway_client.create_user()
        print('Create user response:', create_user_response)

        open_debit_card_account_response = accounts_gateway_client.open_debit_card_account(
            user_id=create_user_response.user.id
        )
        print('Open debit card account response:', open_debit_card_account_response)
        card_id = open_debit_card_account_response.account.cards[0].id

        make_top_up_operation_response = operations_gateway_client.make_top_up_operation(
            card_id=card_id,
            account_id=open_debit_card_account_response.account.id
        )
        print('Make top up operation response:', make_top_up_operation_response)