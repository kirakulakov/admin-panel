from __future__ import annotations
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.utils.singleton import singleton


Postgres: PSQL = ...
session: AsyncSession = ...

@singleton
class PSQL:
    def __init__(self, async_engine: AsyncEngine) -> None:
        self._async_engine = async_engine

    @asynccontextmanager
    async def async_session(self) -> AsyncGenerator[None, AsyncSession]:
        session: AsyncSession = sessionmaker(self._async_engine, class_=AsyncSession, expire_on_commit=False)()

        yield session

    async def test_async_database(self) -> None:
        async with self.async_session() as session:
            await session.execute('SELECT 2')

    async def get_async_session(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session

    async def dispose(self) -> None:
        await self._async_engine.dispose()

    async def commit_or_rollback(self) -> None:
        try:
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


class PSQLBuilder:
    @staticmethod
    def _get_dsn() -> str:
        return f'{settings.psql.user}:{settings.psql.password}@{settings.psql.host}:{settings.psql.port}/{settings.psql.database}'

    @classmethod
    def _build(cls) -> PSQL:
        dsn = cls._get_dsn()
        async_engine = create_async_engine(
            f'postgresql+asyncpg://{dsn}',
            pool_pre_ping=True,
            pool_size=settings.psql.pool_size,
            echo=False)
        return PSQL(async_engine=async_engine)

    @classmethod
    async def build(cls) -> PSQL:
        db = cls._build()
        await db.test_async_database()

        return db


async def get_session() -> AsyncSession:
    return session
