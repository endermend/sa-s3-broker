from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sa_s3_broker.contexts.publication.domain.entities.topic import Topic
from sa_s3_broker.contexts.publication.domain.repositories.topic_repository import (
    ITopicRepository,
)
from sa_s3_broker.contexts.publication.domain.value_objects.password_hash import (
    PasswordHash,
)
from sa_s3_broker.contexts.publication.domain.value_objects.topic_id import TopicID
from sa_s3_broker.contexts.publication.infrastructure.persistance.models.topic_model import (
    TopicORMModel,
)


class TopicRepository(ITopicRepository):
    """Реализация ITopicRepository на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        """Инициализация TopicRepository."""
        self._session = session

    @override
    async def save(self, topic: Topic) -> None:
        """Сохранение Publication."""
        topic_orm = TopicORMModel(
            id=topic.id.value,
            updated_at=topic.updated_at,
            name=topic.name,
            password_hash=topic.password_hash.value,
        )
        await self._session.merge(topic_orm)
        await self._session.commit()

    @override
    async def get_by_id(self, topic_id: TopicID) -> Topic | None:
        topic_orm = await self._session.get(
            TopicORMModel, topic_id.value
        )
        if topic_orm is None:
            return None
        return Topic.hydrate(
            id=TopicID(topic_orm.id),
            name=topic_orm.name,
            password_hash=PasswordHash(topic_orm.password_hash),
            created_at=topic_orm.created_at,
            updated_at=topic_orm.updated_at,
        )

    @override
    async def get_by_name(self, topic_name: str) -> Topic | None:
        stmt = select(TopicORMModel).where(TopicORMModel.name == topic_name)
        result = await self._session.execute(stmt)
        topic_orm = result.scalar()
        if topic_orm is None:
            return None
        return Topic.hydrate(
            id=TopicID(topic_orm.id),
            name=topic_orm.name,
            password_hash=PasswordHash(topic_orm.password_hash),
            created_at=topic_orm.created_at,
            updated_at=topic_orm.updated_at,
        )