from pydantic import Field, field_validator

from src.schemas.v1.response.base import ResponseBase
from src.utils.security import hash_password


class RequestSignUp(ResponseBase):
    login: str = Field(...)
    password: str = Field(...)

    @field_validator('password')
    def hash_password(cls, value: str):
        value = hash_password(value)
        return value
