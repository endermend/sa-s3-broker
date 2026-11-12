from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from sa_s3_broker.infrastructure.config import Config
from sa_s3_broker.infrastructure.di.container import make_container_di
from sa_s3_broker.presentation.api.setup_exception_handlers import (
    setup_exception_handlers,
)
from sa_s3_broker.presentation.api.setup_middleware import setup_middleware
from sa_s3_broker.presentation.api.setup_routers import setup_routers


def create_app() -> FastAPI:
    """
    Создание приложения FastAPI.

    Создается приложение FastAPI, подключаются middleware, routers,
    exception handlers и di

    Returns:
        FastAPI

    """
    config = Config()  # type:ignore[call-arg]
    container = make_container_di(config=config)

    app = FastAPI()

    # Middleware
    setup_middleware(app=app)

    # Routers
    setup_routers(app=app)

    # Exception handlers
    setup_exception_handlers(app=app)

    # Dishka
    setup_dishka(container=container, app=app)

    return app
