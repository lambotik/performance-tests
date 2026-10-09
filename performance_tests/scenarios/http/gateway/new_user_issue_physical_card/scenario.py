from locust import task

from performance_tests.clients.http.gateway.accounts.schema import OpenDebitCardAccountResponseSchema
from performance_tests.clients.http.gateway.locust import GatewayHTTPSequentialTaskSet
from performance_tests.clients.http.gateway.users.schema import CreateUserResponseSchema
from performance_tests.tools.locust.user import LocustBaseUser


class IssuePhysicalCardSequentialTaskSet(GatewayHTTPSequentialTaskSet):
    create_user_response: CreateUserResponseSchema | None = None
    open_open_debit_card_account_response: OpenDebitCardAccountResponseSchema | None = None

    @task
    def create_user(self):
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self):
        if not self.create_user_response:
            return

        self.open_open_debit_card_account_response = self.accounts_gateway_client.open_debit_card_account(
            user_id=self.create_user_response.user.id
        )

    @task
    def issue_physical_card(self):
        if (not self.create_user_response) or (not self.open_open_debit_card_account_response):
            return

        self.cards_gateway_client.issue_physical_card(
            user_id=self.create_user_response.user.id,
            account_id=self.open_open_debit_card_account_response.account.id
        )


class IssuePhysicalCardScenarioUser(LocustBaseUser):
    tasks = [IssuePhysicalCardSequentialTaskSet]
