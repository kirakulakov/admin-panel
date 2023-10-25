from pydantic import Field

from src.infrastructure.db.models.psql.item import DBItem
from src.infrastructure.db.models.psql.user import DBUser
from src.schemas.v1.response.base import ResponseBase


class ResponseUser(ResponseBase):
    id: int = Field(...)
    login: str = Field(...)


class ResponseUserFactory:
    @staticmethod
    def get_from_user(user: DBUser) -> ResponseUser:
        return ResponseUser(
            id=user.id,
            login=user.login
        )

    @classmethod
    def get_many_from_users(cls, users: list[DBUser]) -> list[ResponseUser]:
        return [cls.get_from_user(user=user) for user in users]


class ResponseItem(ResponseBase):
    id: int = Field(...)
    name: str = Field(...)
    account_id: int = Field(...)


class ResponseItemFactory:
    @staticmethod
    def get_from_item(item: DBItem) -> ResponseItem:
        return ResponseItem(
            id=item.id,
            name=item.name,
            account_id=item.account_id
        )

    @classmethod
    def get_many_from_items(cls, items: list[DBItem]) -> list[ResponseItem]:
        return [cls.get_from_item(item=item) for item in items]


class ResponseDashboard(ResponseBase):
    users: list[ResponseUser] = Field([])
    items: list[ResponseItem] = Field([])


class ResponseDashboardFactory:
    @staticmethod
    def get_from_users_and_items(users: list[DBUser], items: list[DBItem]) -> ResponseDashboard:
        return ResponseDashboard(
            users=ResponseUserFactory.get_many_from_users(users=users),
            items=ResponseItemFactory.get_many_from_items(items=items)

        )
