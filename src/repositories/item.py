from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.psql.item import DBItem
from src.repositories.base import PSQLBaseRepository


class ItemRepository(PSQLBaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db)
        self.db = db

    async def get_all(self, limit: int, offset: int) -> list[DBItem]:
        query = select(DBItem).limit(limit).offset(offset)
        return await self.all_ones(query)
