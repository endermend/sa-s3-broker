from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sa_s3_broker.contexts.publication.domain.entities.publication import Publication
from sa_s3_broker.contexts.publication.domain.repositories.publication_repository import (
    IPublicationRepository,
)
from sa_s3_broker.contexts.publication.domain.value_objects.publication_id import (
    PublicationID,
)
from sa_s3_broker.contexts.publication.domain.value_objects.publication_status import (
    PublicationStatus,
)
from sa_s3_broker.contexts.publication.domain.value_objects.topic_id import TopicID
from sa_s3_broker.contexts.publication.infrastructure.persistance.models.publication_model import (
    PublicationORMModel,
)


class PublicationRepository(IPublicationRepository):
    """Реализация IPublicationRepository на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        """Инициализация PublicationRepository."""
        self._session = session

    @override
    async def save(self, publication: Publication) -> None:
        """Сохранение Publication."""
        publication_orm = PublicationORMModel(
            id=publication.id.value,
            updated_at=publication.updated_at,
            topic_id=publication.topic_id.value,
            name=publication.name,
            status=publication.status.to_val(),
        )
        await self._session.merge(publication_orm)
        await self._session.commit()

    @override
    async def get_by_id(self, publication_id: PublicationID) -> Publication | None:
        publication_orm = await self._session.get(
            PublicationORMModel, publication_id.value
        )
        if publication_orm is None:
            return None
        return Publication.hydrate(
            id=PublicationID(publication_orm.id),
            topic_id=TopicID(publication_orm.topic_id),
            name=publication_orm.name,
            status=PublicationStatus.from_val(publication_orm.status),
            created_at=publication_orm.created_at,
            updated_at=publication_orm.updated_at,
        )

    @override
    async def get_publications(
        self, topic_id: TopicID | None = None, get_private: bool = False
    ) -> list[Publication]:
        stmt = select(PublicationORMModel)
        if topic_id is not None:
            stmt = stmt.where(PublicationORMModel.topic_id == topic_id.value)

        if not get_private:
            stmt = stmt.where(
                PublicationORMModel.status == PublicationStatus.PUBLIC.to_val()
            )

        result = await self._session.execute(stmt)
        publications_orm = result.scalars()
        return [
            Publication.hydrate(
                id=PublicationID(publication_orm.id),
                topic_id=TopicID(publication_orm.topic_id),
                name=publication_orm.name,
                status=PublicationStatus.from_val(publication_orm.status),
                created_at=publication_orm.created_at,
                updated_at=publication_orm.updated_at,
            )
            for publication_orm in publications_orm
        ]

    @override
    async def delete_publication(self, publication_id: PublicationID) -> bool:
        publication_orm = await self._session.get(
            PublicationORMModel, publication_id.value
        )
        if publication_orm is None:
            return False
        await self._session.delete(publication_orm)
        return True
