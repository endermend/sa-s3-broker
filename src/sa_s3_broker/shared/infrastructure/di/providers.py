from collections.abc import AsyncGenerator

from arq import ArqRedis
from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from sa_s3_broker.infrastructure.arq import get_arq_pool
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
    """Провайдер для всего связанного с Async requests."""

    @provide(scope=Scope.APP)
    @staticmethod
    def provide_arq_pool() -> ArqRedis:
        return get_arq_pool()


    