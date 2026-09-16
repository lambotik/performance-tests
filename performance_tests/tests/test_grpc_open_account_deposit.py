from performance_tests.clients.grpc.gateway.accounts.client import build_accounts_gateway_grpc_client
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