import uuid

from pydantic import BaseModel, Field, EmailStr


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
    email: str = Field(default_factory=lambda: f"user.{uuid.uuid4()}@example.com")
    lastName: str = "Doe"
    firstName: str = "John"
    middleName: str = "Alexander"
    phoneNumber: str = "+79991234567"
