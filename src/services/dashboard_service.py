from fastapi import HTTPException
from starlette import status

from src.repositories.dasboard import DashboardRepository
from src.schemas.v1.request.dashboard import RequestUpdateEntry, RequestUpdateUser, RequestUpdateItem
from src.services.base import BaseService
from src.services.item_service import ItemService
from src.services.user_service import UserService
from src.utils.async_helpers import gather_with_exception_handling


class DashboardService(BaseService):
    def __init__(self, repository: DashboardRepository):
        super().__init__(repository)
        self.repository = repository

    async def delete_entry(self, user_id: int | None, item_id: int | None) -> None:
        return await self.repository.delete_entry(user_id=user_id, item_id=item_id)

    async def _update_user(
            self,
            user_service: UserService,
            request_model: RequestUpdateUser | None = None,
    ) -> None:
        if request_model:
            user = await user_service.get_by_id(id_=request_model.id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

            if request_model.login:
                user.login = request_model.login

            if request_model.password:
                user.password = request_model.password

    async def _update_item(
            self,
            item_service: ItemService,
            request_model: RequestUpdateItem | None = None,
    ) -> None:

        if request_model:
            item = await item_service.get_by_id(id_=request_model.id)
            if not item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found!")

            if request_model.account_id:
                item.account_id = request_model.account_id

            if request_model.name:
                item.name = request_model.name

    async def update_entry(
            self,
            request_model: RequestUpdateEntry,
            user_service: UserService,
            item_service: ItemService,
    ) -> None:
        await gather_with_exception_handling(
            self._update_item(item_service=item_service, request_model=request_model.item),
            self._update_user(user_service=user_service, request_model=request_model.user)
        )
