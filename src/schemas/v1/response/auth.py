from pydantic import Field

from src.core.config import Secrets
from src.db.models.psql.user import DBUser
from src.schemas.v1.response.base import ResponseBase


class ResponseToken(ResponseBase):
    access_token: str = Field(...)
    token_type: str = Field('bearer')


class ResponseLogin(ResponseToken):
    id: int = Field(...)


class ResponseLoginFactory:
    @staticmethod
    def factory_method(user: DBUser, secrets: Secrets):
        return ResponseLogin(
            id=user.id,
            access_token=user.get_access_token(secrets=secrets),
        )
