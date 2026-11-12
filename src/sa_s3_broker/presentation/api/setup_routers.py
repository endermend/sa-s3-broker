from fastapi import APIRouter, FastAPI

from sa_s3_broker.presentation.api.routers import publication


def setup_routers(app: FastAPI) -> None:
    """Установка роутеров приложения."""
    api_router = APIRouter(prefix="/api")

    api_router.include_router(publication.router)
    app.include_router(api_router)
