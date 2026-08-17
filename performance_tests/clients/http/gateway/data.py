import uuid


class DataPayload:
    @staticmethod
    def user_create_payload():
        return {
            "email": f"user.{uuid.uuid4()}@example.com",
            "lastName": "string",
            "firstName": "string",
            "middleName": "string",
            "phoneNumber": "string",
        }

    @staticmethod
    def make_top_up_operation_payload(
            card_id: str,
            account_id: str,
            status: str = "COMPLETED",
            amount: int = 1500):
        return {
            "status": status,
            "amount": amount,
            "cardId": card_id,
            "accountId": account_id
        }

    @staticmethod
    def make_purchase_operation_payload(
            card_id: str,
            account_id: str,
            category: str,
            status: str = 'IN_PROGRESS',
            amount: float = 77.99, ):
        return {
            "status": status,
            "amount": amount,
            "cardId": card_id,
            "accountId": account_id,
            "category": category
        }

    @staticmethod
    def open_virtual_card_payload(
            user_id: str,
            account_id: str):
        return {
            "userId": user_id,
            "accountId": account_id
        }

    @staticmethod
    def open_physical_card_payload(
            user_id: str,
            account_id: str):
        return {
            "userId": user_id,
            "accountId": account_id
        }
