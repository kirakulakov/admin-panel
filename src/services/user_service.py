from src.db.models.psql.user import DBUser
from src.repositories.user import UserRepository
from src.services.base import BaseService


class UserService(BaseService):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)
        self.repository = repository

    async def get_all(self, limit: int, offset: int) -> list[DBUser]:
        return await self.repository.get_all(limit=limit, offset=offset)

    async def get_by_id(self, id_: int) -> DBUser:
        return await self.repository.get_by_id(id_=id_)
