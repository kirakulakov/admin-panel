from fastapi import APIRouter, Depends

from src.api.depends import get_user_service, get_item_service
from src.schemas.v1.response.dashboard import ResponseDashboardCounters
from src.services.item_service import ItemService
from src.services.user_service import UserService
from src.utils.async_helpers import gather_with_exception_handling

router = APIRouter()


@router.post('/counters', response_model=ResponseDashboardCounters)
async def get_counters(
        user_service: UserService = Depends(get_user_service),
        item_service: ItemService = Depends(get_item_service),
):
    count_users, count_items = await gather_with_exception_handling(
        user_service.get_count(),
        item_service.get_count()
    )

    return ResponseDashboardCounters(count_users=count_users, count_items=count_items)
