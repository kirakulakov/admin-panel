from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select, Delete

from src.db.models.psql.base import BaseModel


class PSQLBaseRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    # async def _commit_or_rollback(self):
    #     try:
    #         await self._db.commit()
    #     except Exception:
    #         await self._db.rollback()
    #         raise
    #     finally:
    #         await self._db.close()

    async def one_or_none(self, query: Select) -> Any:
        result = await self._db.execute(query)
        result = result.one_or_none()
        if not result:
            return None
        return result[0]

    async def one_val(self, query: Select) -> Any:
        result = await self._db.execute(query)
        result = result.one()
        return result[0]

    async def add_model(self, model: BaseModel) -> None:
        self._db.add(model)
        await self._db.flush([model])
        # await self._commit_or_rollback()

    async def all_ones(self, query: Select) -> list[Any]:
        result = await self._db.execute(query)
        return [row[0] for row in result.all()]

    async def execute_fetch(self, query: Delete) -> None:
        await self._db.execute(query)
        # await self._commit_or_rollback()
