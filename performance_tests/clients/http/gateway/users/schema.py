import uuid

from pydantic import BaseModel, Field, EmailStr, ConfigDict

from performance_tests.tools.fakers import fake


class User(BaseModel):
    id: uuid.UUID = Field(..., description="User identifier")
    email: EmailStr = Field(..., description="User email")
    last_name: str = Field(..., alias="lastName", description="Last name")
    first_name: str = Field(..., alias="firstName", description="First name")
    middle_name: str = Field(..., alias="middleName", description="Middle name")
    phone_number: str = Field(..., alias="phoneNumber", description="Phone number")


class CreateUserResponseSchema(BaseModel):
    user: User


class CreateUserRequestSchema(BaseModel):
    """
    Структура данных для создания нового пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    # Добавили генерацию случайного email
    email: EmailStr = Field(default_factory=fake.email)
    # Добавили генерацию случайной фамилии
    last_name: str = Field(alias="lastName", default_factory=fake.last_name)
    # Добавили генерацию случайного имени
    first_name: str = Field(alias="firstName", default_factory=fake.first_name)
    # Добавили генерацию случайного отчества
    middle_name: str = Field(alias="middleName", default_factory=fake.middle_name)
    # Добавили генерацию случайного номер телефона
    phone_number: str = Field(alias="phoneNumber", default_factory=fake.phone_number)
