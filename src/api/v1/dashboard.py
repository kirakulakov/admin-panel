from fastapi import APIRouter, Depends, Query

from src.api.depends import get_user_service, get_item_service, PagesPaginationParams, get_user_id_from_token, \
    get_dashboard_service
from src.schemas.v1.request.dashboard import RequestUpdateEntry, RequestAddEntry
from src.schemas.v1.response.base import ResponseEmpty
from src.schemas.v1.response.dashboard import ResponseDashboard, ResponseDashboardFactory
from src.services.dashboard_service import DashboardService
from src.services.item_service import ItemService
from src.services.user_service import UserService

router = APIRouter()


@router.get('/entries', response_model=ResponseDashboard)
async def get_entries(
        user_service: UserService = Depends(get_user_service),
        item_service: ItemService = Depends(get_item_service),
        dashboard_service: DashboardService = Depends(get_dashboard_service),
        pagination_params: PagesPaginationParams = Depends(),
        _=Depends(get_user_id_from_token)
):
    users, items = await dashboard_service.get_entries(
        user_service=user_service, item_service=item_service,
        limit=pagination_params.limit, offset=pagination_params.offset)

    return ResponseDashboardFactory.get_from_users_and_items(users=users, items=items)


@router.delete('/entries', response_model=ResponseEmpty)
async def delete_entry(
        user_id: int | None = Query(None),
        item_id: int | None = Query(None),
        dashboard_service: DashboardService = Depends(get_dashboard_service),
        _=Depends(get_user_id_from_token)
):
    await dashboard_service.delete_entry(user_id=user_id, item_id=item_id)
    return ResponseEmpty()


@router.patch('/entries', response_model=ResponseEmpty)
async def update_entry(
        request_model: RequestUpdateEntry,
        dashboard_service: DashboardService = Depends(get_dashboard_service),
        user_service: UserService = Depends(get_user_service),
        item_service: ItemService = Depends(get_item_service),
        _=Depends(get_user_id_from_token)
):
    await dashboard_service.update_entry(
        request_model=request_model, user_service=user_service, item_service=item_service)
    return ResponseEmpty()


@router.post('/entries', response_model=ResponseEmpty)
async def add_entry(
        request_model: RequestAddEntry,
        dashboard_service: DashboardService = Depends(get_dashboard_service),
        _=Depends(get_user_id_from_token)
):
    await dashboard_service.add_entry(
        request_model=request_model)
    return ResponseEmpty()
