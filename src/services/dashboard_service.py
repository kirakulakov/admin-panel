from src.repositories.dasboard import DashboardRepository
from src.schemas.v1.request.dashboard import RequestUpdateEntry
from src.services.base import BaseService


class DashboardService(BaseService):
    def __init__(self, repository: DashboardRepository):
        super().__init__(repository)
        self.repository = repository

    async def delete_entry(self, user_id: int | None, item_id: int | None) -> None:
        return await self.repository.delete_entry(user_id=user_id, item_id=item_id)

    async def update_entry(self, request_model: RequestUpdateEntry) -> None:
        return await self.repository.update_entry(request_model=request_model)
