from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from starlette import status

from src.connections.psql import get_session
from src.core.config import settings
from src.repositories.item import ItemRepository
from src.repositories.user import UserRepository
from src.services.auth_service import AuthService
from src.services.item_service import ItemService
from src.services.user_service import UserService

# TODO change url
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
