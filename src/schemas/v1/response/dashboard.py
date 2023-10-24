from pydantic import Field

from src.schemas.v1.response.base import ResponseBase


class ResponseDashboardCounters(ResponseBase):
    count_users: int = Field(...)
    count_items: int = Field(...)
