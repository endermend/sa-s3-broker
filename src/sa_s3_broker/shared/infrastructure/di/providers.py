from collections.abc import AsyncGenerator

from dishka import (
    Provider,
    Scope,
    provide,
)
from redis.client import Redis
from rq import Queue
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from sa_s3_broker.infrastructure.config import Config
from sa_s3_broker.shared.infrastructure.persistence.session import (
    new_async_session_maker,
)


class DBProvider(Provider):
    """Провайдер для всего связанного с БД."""

    @provide(scope=Scope.APP)
    @staticmethod
    def get_session_maker(config: Config) -> async_sessionmaker[AsyncSession]:
        """
        Провайдер для async_sessionmaker[AsyncSession].

        Returns:
            async_sessionmaker[AsyncSession]

        """
        return new_async_session_maker(db_config=config.DB)

    @provide(scope=Scope.REQUEST)
    @staticmethod
    async def get_session(
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncGenerator[AsyncSession]:
        """
        Провайдер сессии.

        Yields:
            Iterator[AsyncIterable[AsyncSession]]

        """
        async with session_maker() as session:
            yield session

class RQProvider(Provider):
    """Провайдер для всего связанного с Redis."""

    @provide(scope=Scope.APP)
    @staticmethod
    def get_redis(config: Config) -> Redis:
        """
        Провайдер для Redis.

        Returns:
            Redis

        """
        return Redis(
            host=config.REDIS.HOST,
            port=config.REDIS.PORT,
            password=config.REDIS.PASSWORD,
            decode_responses=True,
        )

    @provide(scope=Scope.APP)
    @staticmethod
    def get_queue(redis: Redis) -> Queue:
        """
        Провайдер для Redis.

        Returns:
            Redis

        """
        return Queue(connection=redis)
    