from performance_tests.clients.http.helpers import HTTPClientHelpers
from performance_tests.conftest import  api_helper

class TestHttpxApi:
    def test_open_deposit_account(self, api_helper: HTTPClientHelpers):
        create_user_response = api_helper.post_create_user()
        create_user_response_data = create_user_response.json()
        user_id = create_user_response_data["user"]["id"]
        open_deposit_account_response = api_helper.post_open_deposit_account(user_id=user_id)
        assert open_deposit_account_response.status_code is 200
        print("Open deposit account response:", open_deposit_account_response.json())

    def test_create_virtual_card(self, api_helper: HTTPClientHelpers):
        create_user_response = api_helper.post_create_user()
        assert create_user_response.status_code is 200, 'User is not created'
        create_user_response_data = create_user_response.json()
        user_id = create_user_response_data["user"]["id"]
        open_debit_card_account_response = api_helper.post_open_debit_card_account(user_id=user_id)
        account_id = open_debit_card_account_response.json()["account"]["id"]
        assert open_debit_card_account_response.status_code is 200, 'Debit card is not created'
        create_virtual_card_response = api_helper.post_open_virtual_card(user_id, account_id)
        assert create_virtual_card_response.status_code is 200, 'Virtual card is not created'
        print(create_virtual_card_response.json())

    def test_get_document(self, api_helper: HTTPClientHelpers):
        create_user_response = api_helper.post_create_user()
        assert create_user_response.status_code is 200, 'User is not created'
        user_id = create_user_response.json()["user"]["id"]
        response_open_credit_card_account = api_helper.post_open_credit_card_account(user_id)
        print(response_open_credit_card_account.json())
        assert response_open_credit_card_account.status_code is 200
        account_id = response_open_credit_card_account.json()["account"]["id"]
        response_get_tariff = api_helper.get_tariff_document(account_id)
        print(response_get_tariff.json())
        assert response_get_tariff.status_code is 200
        response_get_contract_document = api_helper.get_contract_document(account_id)
        print(response_get_contract_document.json())
        assert response_get_contract_document.status_code is 200

    def test_make_top_up_operation(self, api_helper: HTTPClientHelpers):
        create_user_response = api_helper.post_create_user()
        assert create_user_response.status_code is 200, 'User is not created'
        user_id = create_user_response.json()["user"]["id"]
        response_open_debit_card_account = api_helper.post_open_debit_card_account(user_id=user_id)
        card_id = response_open_debit_card_account.json()["account"]["cards"][0]["id"]
        account_id = response_open_debit_card_account.json()["account"]["id"]
        response_make_top_up_operation = api_helper.post_make_top_up_operation(account_id=account_id, card_id=card_id)
        assert response_make_top_up_operation.status_code is 200
        print(response_make_top_up_operation.json())

    def test_make_purchase_operation(self, api_helper: HTTPClientHelpers):
        create_user_response = api_helper.post_create_user()
        assert create_user_response.status_code is 200, 'User is not created'
        user_id = create_user_response.json()["user"]["id"]
        response_open_debit_card_account = api_helper.post_open_debit_card_account(user_id=user_id)
        card_id = response_open_debit_card_account.json()["account"]["cards"][0]["id"]
        account_id = response_open_debit_card_account.json()["account"]["id"]
        response_make_purchase_operation = api_helper.post_make_purchase_operation(
            account_id=account_id,
            card_id=card_id,
            status='IN_PROGRESS',
            amount=77.99,
            category='taxi')
        operation_id = response_make_purchase_operation.json()['operation']['id']
        response_operation_receipt = api_helper.get_operation_receipt(operation_id=operation_id)
        assert response_operation_receipt.status_code is 200
        print(response_operation_receipt.json())
