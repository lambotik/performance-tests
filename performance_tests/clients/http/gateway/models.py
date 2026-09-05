import uuid
from typing import Dict, Any

from pydantic import BaseModel, Field, EmailStr


class DataPayload:
    """
    Фабрика для генерации тестовых данных (payload) запросов к API.
    Централизует создание словарей с валидными дефолтными значениями
    и динамической генерацией уникальных данных (например, email).
    """

    @staticmethod
    def user_create_payload() -> Dict[str, Any]:
        """
        Генерирует валидный payload для создания нового пользователя.
        Автоматически создает уникальный email и подставляет безопасные
        дефолтные значения для остальных полей.
        :return: Словарь с данными пользователя, готовый к отправке в API.
        """
        payload = CreateUserRequestDict()
        return payload.model_dump()

    @staticmethod
    def make_top_up_operation_payload(
            card_id: str,
            account_id: str,
            status: str = "COMPLETED",
            amount: int = 1500
    ) -> Dict[str, Any]:
        """
        Создает payload для операции пополнения счета (Top-Up).
        :param card_id: Идентификатор карты, участвующей в операции.
        :param account_id: Идентификатор счета.
        :param status: Статус операции (по умолчанию "COMPLETED").
        :param amount: Сумма пополнения в условных единицах (по умолчанию 1500).
        :return: Словарь с данными операции пополнения.
        """
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
            amount: float = 77.99,
    ) -> Dict[str, Any]:
        """
        Создает payload для операции покупки (списание средств).
        :param card_id: Идентификатор карты, с которой происходит списание.
        :param account_id: Идентификатор счета, привязанного к карте.
        :param category: Категория трат (обязательный параметр, например, "GROCERIES").
        :param status: Статус операции (по умолчанию "IN_PROGRESS")
         Доступные статусы:``["FAILED", "COMPLETED","IN_PROGRESS", "UNSPECIFIED"]``
        :param amount: Сумма покупки (по умолчанию 77.99).
        :return: Словарь с данными операции покупки.
        """
        return {
            "status": status,
            "amount": amount,
            "cardId": card_id,
            "accountId": account_id,
            "category": category
        }

    @staticmethod
    def open_virtual_card_payload(user_id: str, account_id: str) -> Dict[str, Any]:
        """
        Создает payload для запроса на выпуск виртуальной карты.
        :param user_id: Идентификатор пользователя, которому выпускается карта.
        :param account_id: Идентификатор счета, к которому будет привязана карта.
        :return: Словарь с данными для выпуска виртуальной карты.
        """
        return {
            "userId": user_id,
            "accountId": account_id
        }

    @staticmethod
    def open_physical_card_payload(user_id: str, account_id: str) -> Dict[str, Any]:
        """
        Создает payload для запроса на выпуск физической карты.
        :param user_id: Идентификатор пользователя, которому выпускается карта.
        :param account_id: Идентификатор счета, к которому будет привязана карта.
        :return: Словарь с данными для выпуска физической карты.
        """
        return {
            "userId": user_id,
            "accountId": account_id
        }


class User(BaseModel):
    id: uuid.UUID = Field(..., description="User identifier")
    email: EmailStr = Field(..., description="User email")
    lastName: str = Field(..., description="Last name")
    firstName: str = Field(..., description="First name")
    middleName: str = Field(..., description="Middle name")
    phoneNumber: str = Field(..., description="Phone number")


class CreateUserResponseSchema(BaseModel):
    user: User


class CreateUserRequestDict(BaseModel):
    email: str = Field(default_factory=lambda: f"user.{uuid.uuid4()}@example.com")
    lastName: str = "Doe"
    firstName: str = "John"
    middleName: str = "Alexander"
    phoneNumber: str = "+79991234567"


class MakePurchaseOperationRequestDict(BaseModel):
    status: str
    amount: int | float
    cardId: str
    accountId: str
    category: str


class MakeTopUpOperationRequestDict(BaseModel):
    status: str
    amount: int | float
    cardId: str
    accountId: str


class IssueVirtualCardRequestDict(BaseModel):
    """
    Структура данных для выпуска виртуальной карты.
    """
    userId: str
    accountId: str


class IssuePhysicalCardRequestDict(BaseModel):
    """
    Структура данных для выпуска физической карты.
    """
    userId: str
    accountId: str


class GetAccountsQueryDict(BaseModel):
    """
    Структура данных для получения списка счетов пользователя.
    """
    userId: str


class OpenDepositAccountRequestDict(BaseModel):
    """
    Структура данных для открытия депозитного счета.
    """
    userId: str


class OpenSavingsAccountRequestDict(BaseModel):
    """
    Структура данных для открытия сберегательного счета.
    """
    userId: str


class OpenDebitCardAccountRequestDict(BaseModel):
    """
    Структура данных для открытия дебетового счета.
    """
    userId: str


class OpenCreditCardAccountRequestDict(BaseModel):
    """
    Структура данных для открытия кредитного счета.
    """
    userId: str
