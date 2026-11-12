import asyncio

try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from arq.connections import RedisSettings
from dishka.integrations.arq import setup_dishka

from sa_s3_broker.contexts.publication.application.tasks import (
    check_expiration_task,
)
from sa_s3_broker.infrastructure.config import Config
from sa_s3_broker.infrastructure.di.container import make_container_di


def _build_redis_settings(config: Config) -> RedisSettings:
    """Создать настройки Redis для воркера ARQ."""
    return RedisSettings(
        host=config.REDIS.HOST,
        port=config.REDIS.PORT,
        password=config.REDIS.PASSWORD,
    )


config = Config()  # type: ignore[call-arg]
container = make_container_di(config=config)


class WorkerSettings:
    """Настройки воркера ARQ."""

    functions = [check_expiration_task]  # noqa: RUF012

    redis_settings = _build_redis_settings(config)

    max_jobs = 10

    job_timeout = 300


setup_dishka(container=container, worker_settings=WorkerSettings)
