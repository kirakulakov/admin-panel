from fastapi import APIRouter, Depends, Query

from src.api.depends import get_user_service, get_item_service, PagesPaginationParams, get_user_id_from_token, \
    get_dashboard_service
from src.schemas.v1.request.dashboard import RequestUpdateEntry
from src.schemas.v1.response.base import ResponseEmpty
from src.schemas.v1.response.dashboard import ResponseDashboard, ResponseDashboardFactory
from src.services.dashboard_service import DashboardService
from src.services.item_service import ItemService
from src.services.user_service import UserService
from src.utils.async_helpers import gather_with_exception_handling

router = APIRouter()


@router.post('/', response_model=ResponseDashboard)
async def get_entries(
        user_service: UserService = Depends(get_user_service),
        item_service: ItemService = Depends(get_item_service),
        pagination_params: PagesPaginationParams = Depends(),
        _ = Depends(get_user_id_from_token)
):
    users, items = await gather_with_exception_handling(
        user_service.get_all(limit=pagination_params.limit, offset=pagination_params.offset),
        item_service.get_all(limit=pagination_params.limit, offset=pagination_params.offset)
    )

    return ResponseDashboardFactory.get_from_users_and_items(users=users, items=items)


@router.delete('/', response_model=ResponseEmpty)
async def delete_entry(
        user_id: int | None = Query(None),
        item_id: int | None = Query(None),
        dashboard_service: DashboardService = Depends(get_dashboard_service),
        _ = Depends(get_user_id_from_token)
):
    await dashboard_service.delete_entry(user_id=user_id, item_id=item_id)
    return ResponseEmpty()


@router.patch('/', response_model=ResponseEmpty)
async def update_entry(
        request_model: RequestUpdateEntry,
        dashboard_service: DashboardService = Depends(get_dashboard_service),
        user_service: UserService = Depends(get_user_service),
        item_service: ItemService = Depends(get_item_service),
        _ = Depends(get_user_id_from_token)
):
    await dashboard_service.update_entry(
        request_model=request_model, user_service=user_service, item_service=item_service)
    return ResponseEmpty()