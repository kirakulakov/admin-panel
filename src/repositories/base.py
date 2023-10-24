from abc import ABC
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from src.db.models.psql.base import BaseModel


class PSQLBaseRepository(ABC):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def one_or_none(self, query: Select) -> Any:
        result = await self.db.execute(query)
        result = result.one_or_none()
        if not result:
            return None
        return result[0]

    async def one_val(self, query: Select) -> Any:
        result = await self.db.execute(query)
        result = result.one()
        return result[0]

    async def add_model(self, model: BaseModel) -> None:
        self.db.add(model)
        await self.db.flush([model])

        try:
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise
        finally:
            await self.db.close()
