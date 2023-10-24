import uvicorn as uvicorn

from src.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        'src.api.app:app',
        host=settings.server.host,
        port=settings.server.port,
        log_level=settings.server.log_level,
        reload=settings.server.reload,
        proxy_headers=settings.server.proxy_headers,
        workers=settings.server.workers
    )
