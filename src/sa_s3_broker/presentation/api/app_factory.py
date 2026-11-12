from contextlib import asynccontextmanager

from arq.connections import RedisSettings
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from sa_s3_broker.infrastructure.arq import close_arq, init_arq
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

    @asynccontextmanager
    async def lifespan(app: FastAPI, /):
        redis_settings = RedisSettings(
            host=config.REDIS.HOST,
            port=config.REDIS.PORT,
            password=config.REDIS.PASSWORD,
        )
        await init_arq(redis_settings)

        yield

        await close_arq()
        await container.close()

    app = FastAPI(lifespan=lifespan)

    # Middleware
    setup_middleware(app=app)

    # Routers
    setup_routers(app=app)

    # Exception handlers
    setup_exception_handlers(app=app)

    # Dishka
    setup_dishka(container=container, app=app)

    return app
