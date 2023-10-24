from src.repositories.item import ItemRepository
from src.services.base import BaseService


class ItemService(BaseService):
    def __init__(self, repository: ItemRepository):
        super().__init__(repository)
        self.repository = repository

    async def get_count(self) -> int:
        return await self.repository.get_all_count()
