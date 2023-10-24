from sqlalchemy import Column, VARCHAR, Integer, ForeignKey

from src.db.models.psql.base import BaseModel


class DBItem(BaseModel):
    __tablename__ = 'item'

    account_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    name = Column(VARCHAR(255), nullable=False)


class DBItemFactory:
    @staticmethod
    def create_new(account_id: int, name: str) -> DBItem:
        return DBItem(account_id=account_id, name=name)
