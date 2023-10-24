from pydantic import Field, field_validator

from src.schemas.v1.request.base import RequestBase
from src.utils.security import hash_password


class RequestUpdateUser(RequestBase):
    id: int = Field(...)
    login: str | None = Field(None)
    password: str | None = Field(None)

    @field_validator('password')
    def hash_password(cls, value: str | None):
        if not value:
            return value

        value = hash_password(value)
        return value


class RequestUpdateItem(RequestBase):
    id: int = Field(...)
    account_id: int | None = Field(None)
    name: str | None = Field(None)


class RequestUpdateEntry(RequestBase):
    user: RequestUpdateUser | None = Field(None)
    item: RequestUpdateItem | None = Field(None)


class RequestAddUser(RequestBase):
    login: str = Field(None)
    password: str | None = Field(None)

    @field_validator('password')
    def hash_password(cls, value: str | None):
        if not value:
            return value

        value = hash_password(value)
        return value


class RequestAddItem(RequestBase):
    account_id: int = Field(...)
    name: str = Field(...)


class RequestAddEntry(RequestBase):
    user: RequestAddUser | None = Field(None)
    item: RequestAddItem | None = Field(None)
