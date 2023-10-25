from src.infrastructure.db.models.psql.item import DBItem
from src.repositories.item import ItemRepository
from src.services.base import BaseService


class ItemService(BaseService):
    def __init__(self, repository: ItemRepository):
        super().__init__(repository)
        self.repository = repository

    async def get_all(self, limit: int, offset: int) -> list[DBItem]:
        return await self.repository.get_all(limit=limit, offset=offset)

    async def get_by_id(self, id_: int) -> DBItem | None:
        return await self.repository.get_by_id(id_=id_)
