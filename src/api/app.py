from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from h11 import Request

from src.api.v1.router import router as v1_router
from src.connections import psql
from src.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    psql.Postgres = await psql.PSQLBuilder.build()

    async with psql.Postgres.async_session() as session:
        psql.session = session

    yield

    await psql.Postgres.dispose()
    await session.close()


app = FastAPI(
    title='admin-panel',
    lifespan=lifespan,
    docs_url=settings.server.docs_url,
    openapi_url=settings.server.openapi_url,
    default_response_class=ORJSONResponse
)

app.include_router(v1_router, tags=['v1'])


@app.middleware("http")
async def http_middleware(request: Request, call_next):
    response = await call_next(request)
    await psql.Postgres.commit_or_rollback()

    return response
