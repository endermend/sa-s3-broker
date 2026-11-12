from collections.abc import AsyncIterable

from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from sa_s3_broker.contexts.publication.domain.repositories.publication_repository import (
    IPublicationRepository,
)
from sa_s3_broker.contexts.publication.domain.repositories.topic_repository import (
    ITopicRepository,
)
from sa_s3_broker.contexts.publication.infrastructure.persistance.repositories.publication_repository import (
    PublicationRepository,
)
from sa_s3_broker.contexts.publication.infrastructure.persistance.repositories.topic_repository import (
    TopicRepository,
)


class PublicationDBProvider(Provider):
    """Провайдер бд авторизации."""

    @provide(scope=Scope.REQUEST)
    @staticmethod
    async def get_publication_repository(
        session: AsyncSession,
    ) -> AsyncIterable[IPublicationRepository]:
        """
        Провайдер репозитория публикаций.

        Yields:
            Iterator[AsyncIterable[IUserRepository]]

        """
        yield PublicationRepository(session=session)

    @provide(scope=Scope.REQUEST)
    @staticmethod
    async def get_topic_repository(
        session: AsyncSession,
    ) -> AsyncIterable[ITopicRepository]:
        """
        Провайдер репозитория топиков.

        Yields:
            Iterator[AsyncIterable[IUserRepository]]

        """
        yield TopicRepository(session=session)
