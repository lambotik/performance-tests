from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


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
