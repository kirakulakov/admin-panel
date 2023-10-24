from fastapi import HTTPException
from starlette import status

from src.db.models.psql.item import DBItemFactory, DBItem
from src.db.models.psql.user import DBUserFactory, DBUser
from src.repositories.dasboard import DashboardRepository
from src.schemas.v1.request.dashboard import RequestUpdateEntry, RequestUpdateUser, RequestUpdateItem, RequestAddEntry, \
    RequestAddUser, RequestAddItem
from src.services.base import BaseService
from src.services.item_service import ItemService
from src.services.user_service import UserService
from src.utils.async_helpers import gather_with_exc_handling


class DashboardService(BaseService):
    def __init__(self, repository: DashboardRepository):
        super().__init__(repository)
        self.repository = repository

    async def get_entries(
            self,
            user_service: UserService,
            item_service: ItemService,
            limit: int,
            offset: int
    ) -> tuple[list[DBUser], list[DBItem]]:
        users, items = await gather_with_exc_handling(
            user_service.get_all(limit=limit, offset=offset),
            item_service.get_all(limit=limit, offset=offset)
        )
        return users, items

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
        await gather_with_exc_handling(
            self._update_item(item_service=item_service, request_model=request_model.item),
            self._update_user(user_service=user_service, request_model=request_model.user)
        )

    async def _add_user(
            self,
            request_model: RequestAddUser | None = None
    ) -> DBUser | None:
        if request_model:
            model: DBUser = DBUserFactory.create_new(login=request_model.login, password=request_model.password)
            return model
        return None

    async def _add_item(
            self,
            request_model: RequestAddItem | None = None
    ) -> DBItem | None:

        if request_model:
            model: DBItem = DBItemFactory.create_new(account_id=request_model.account_id, name=request_model.name)
            return model
        return None

    async def add_entry(
            self,
            request_model: RequestAddEntry
    ) -> None:
        models = [
            await self._add_item(request_model=request_model.item),
            await self._add_user(request_model=request_model.user)
        ]
        await self.repository.add_models([model for model in models if model is not None])
