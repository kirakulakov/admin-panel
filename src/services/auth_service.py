from fastapi import HTTPException
from starlette import status

from src.db.models.psql.user import DBUser, DBUserFactory
from src.repositories.user import UserRepository
from src.services.base import BaseService
from src.utils.security import verify


class AuthService(BaseService):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)
        self.repository = repository

    async def _create_new_user(self, login: str, password: str) -> DBUser:
        login_already_registered = await self.repository.check_login_already_register(login=login)
        if login_already_registered:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Login is already registered in the system!")

        user = DBUserFactory.create_new(login=login, password=password)
        await self.repository.add_model(user)
        return user

    async def sign_in(self, login: str, password: str) -> DBUser:
        user = await self.repository.get_by_login(login=login)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if not verify(password=password, user_hashed_password=user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return user

    async def sign_up(self, login: str, password: str) -> None:
        await self._create_new_user(login=login, password=password)
