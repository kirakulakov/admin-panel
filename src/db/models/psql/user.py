from datetime import datetime, timedelta

from jose import jwt
from sqlalchemy import Column, VARCHAR, UniqueConstraint

from src.core.config import Secrets
from src.db.models.psql.base import BaseModel


class DBUser(BaseModel):
    __tablename__ = 'users'

    login = Column(VARCHAR(255), nullable=False, unique=True)
    password = Column(VARCHAR(255), nullable=False)

    def get_access_token(self, secrets: Secrets, life_time_days: int = 7) -> str:
        payload = {
            'sub': f"{self.id}",
            'exp': datetime.now() + timedelta(days=life_time_days),
        }

        return jwt.encode(payload, secrets.secret_key, algorithm=secrets.encrypt_algorithm)


class DBUserFactory:
    @staticmethod
    def create_new(login: str, password: str) -> DBUser:
        return DBUser(login=login, password=password)