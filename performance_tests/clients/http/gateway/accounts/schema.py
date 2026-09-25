import uuid
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from performance_tests.clients.http.gateway.cards.schema import CardSchema


class Account(BaseModel):
    """Схема счёта."""
    model_config = ConfigDict(populate_by_name=True)

    id: uuid.UUID = Field(..., description="Account identifier")
    type: str = Field(..., description="Account type")
    cards: list[CardSchema] = Field(..., description="List of cards")
    status: str = Field(..., description="Account status")
    balance: float = Field(..., description="Account balance")


class GetAccountsQuerySchema(BaseModel):
    """
    Структура данных для получения списка счетов пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str | UUID = Field(..., alias="userId", description="User Id")


class OpenDepositAccountRequestSchema(BaseModel):
    """
    Структура данных для открытия депозитного счета.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str | UUID = Field(..., alias="userId", description="User Id")


class OpenSavingsAccountRequestSchema(BaseModel):
    """
    Структура данных для открытия сберегательного счета.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str | UUID = Field(..., alias="userId", description="User Id")


class OpenSavingsAccountResponseSchema(BaseModel):
    """
    Структура данных ответа на открытие сберегательного счёта.
    """
    account: Account


class OpenDebitCardAccountRequestSchema(BaseModel):
    """
    Структура данных для открытия дебетового счета.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str | UUID = Field(..., alias="userId", description="User Id")


class OpenCreditCardAccountRequestSchema(BaseModel):
    """
    Структура данных для открытия кредитного счета.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str | UUID = Field(..., alias="userId", description="User Id")
