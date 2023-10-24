from src.repositories.item import ItemRepository
from src.repositories.user import UserRepository
from src.services.base import BaseService


class UserService(BaseService):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)
        self.repository = repository

    async def get_count(self) -> int:
        return await self.repository.get_all_count()
