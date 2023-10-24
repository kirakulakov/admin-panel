from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.psql.user import DBUser
from src.repositories.base import PSQLBaseRepository


class UserRepository(PSQLBaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db)
        self.db = db

    async def get_user_by_login(self, login: str) -> DBUser | None:
        query = select(DBUser).where(DBUser.login == login)
        return await self.one_or_none(query)

    async def check_login_already_register(self, login: str) -> bool:
        query = select(DBUser.id).where(DBUser.login == login)
        result = await self.one_or_none(query)
        return result is not None

    async def get_all_count(self) -> int:
        query = select(func.count(DBUser.id))
        return await self.one_val(query)
