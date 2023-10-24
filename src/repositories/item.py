from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.psql.item import DBItem
from src.repositories.base import PSQLBaseRepository


class ItemRepository(PSQLBaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db)
        self.db = db

    async def get_all_count(self) -> int:
        query = select(func.count(DBItem.id))
        return await self.one_val(query)
