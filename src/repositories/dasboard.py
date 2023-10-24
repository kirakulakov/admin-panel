from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.psql.item import DBItem
from src.db.models.psql.user import DBUser
from src.repositories.base import PSQLBaseRepository
from src.schemas.v1.request.dashboard import RequestUpdateEntry
from src.utils.async_helpers import gather_with_exception_handling


class DashboardRepository(PSQLBaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db)
        self.db = db

    async def delete_entry(self, user_id: int | None, item_id: int | None) -> None:
        queries = []
        if user_id:
            query = delete(DBUser).where(DBUser.id == user_id)
            queries.append(self.execute_fetch(query))

        if item_id:
            query = delete(DBItem).where(DBItem.id == item_id)
            queries.append(self.execute_fetch(query))
        await gather_with_exception_handling(*queries)
    #
    #
    # async def update_entry(self, request_model: RequestUpdateEntry) -> None:
    #     queries = []
    #     if user_id:
    #         query = delete(DBUser).where(DBUser.id == user_id)
    #         queries.append(self.execute_fetch(query))
    #
    #     if item_id:
    #         query = delete(DBItem).where(DBItem.id == item_id)
    #         queries.append(self.execute_fetch(query))
    #     await gather_with_exception_handling(*queries)
