from pydantic import BaseModel, ConfigDict, Field


class IssueVirtualCardRequestSchema(BaseModel):
    """
    Структура данных для выпуска виртуальной карты.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str = Field(..., alias="userId", description="User Id")
    account_id: str = Field(..., alias="accountId", description="Account Id")


class IssuePhysicalCardRequestSchema(BaseModel):
    """
    Структура данных для выпуска физической карты.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str = Field(..., alias="userId", description="User Id")
    account_id: str = Field(..., alias="accountId", description="Account Id")