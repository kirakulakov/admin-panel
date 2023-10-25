from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.params import Query
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from starlette import status

from src.core.config import settings
from src.infrastructure.connections.psql import get_session
from src.repositories.dasboard import DashboardRepository
from src.repositories.item import ItemRepository
from src.repositories.user import UserRepository
from src.services.auth_service import AuthService
from src.services.dashboard_service import DashboardService
from src.services.item_service import ItemService
from src.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/sign-in")


class UserId(BaseModel):
    id: int


def decode_token(token):
    try:
        payload = jwt.decode(token, settings.secrets.secret_key, algorithms=[settings.secrets.encrypt_algorithm])
        id_: int = int(payload.get('sub'))  # type: ignore
    except (JWTError, AttributeError, ValueError):
        raise HTTPException(status_code=401, detail="Authorization failed!")

    return UserId(id=id_)


async def get_user_id_from_token(
        token: Annotated[str, Depends(oauth2_scheme)]
):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


class PagesPaginationParams:
    def __init__(
            self,
            limit: int = Query(50, ge=0, le=1_000),
            offset: int = Query(0, ge=0, alias='skip'),
    ) -> None:
        self.limit = limit
        self.offset = offset


@lru_cache()
def get_user_repository(db=Depends(get_session)) -> UserRepository:
    return UserRepository(db=db)


@lru_cache()
def get_item_repository(db=Depends(get_session)) -> ItemRepository:
    return ItemRepository(db=db)


@lru_cache()
def get_auth_service(repository=Depends(get_user_repository)) -> AuthService:
    return AuthService(repository=repository)


@lru_cache()
def get_user_service(repository=Depends(get_user_repository)) -> UserService:
    return UserService(repository=repository)


@lru_cache()
def get_item_service(repository=Depends(get_item_repository)) -> ItemService:
    return ItemService(repository=repository)


@lru_cache()
def get_dashboard_repository(db=Depends(get_session)) -> DashboardRepository:
    return DashboardRepository(db=db)


@lru_cache()
def get_dashboard_service(repository=Depends(get_dashboard_repository)) -> DashboardService:
    return DashboardService(repository=repository)
