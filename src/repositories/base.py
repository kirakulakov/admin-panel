from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select, Delete

from src.infrastructure.db.models.psql.base import BaseModel


class PSQLBaseRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def one_or_none_val(self, query: Select) -> Any:
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

    async def add_models(self, models: list[BaseModel]) -> None:
        self._db.add_all(models)
        await self._db.flush([*models])

    async def all_ones(self, query: Select) -> list[Any]:
        result = await self._db.execute(query)
        return [row[0] for row in result.all()]

    async def execute_fetch(self, query: Delete) -> None:
        await self._db.execute(query)
