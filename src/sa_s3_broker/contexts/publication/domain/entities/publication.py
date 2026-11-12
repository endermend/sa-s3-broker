from dataclasses import dataclass
from datetime import UTC, datetime

from sa_s3_broker.contexts.publication.domain.value_objects.publication_id import (
    PublicationID,
)
from sa_s3_broker.contexts.publication.domain.value_objects.publication_status import (
    PublicationStatus,
)
from sa_s3_broker.contexts.publication.domain.value_objects.topic_id import TopicID
from sa_s3_broker.shared.domain.base_entity import BaseEntity


@dataclass(slots=True)
class Publication(BaseEntity[PublicationID]):
    """Доменная сущность публикации (Entity DDD)."""

    _topic_id: TopicID
    _name: str
    _status: PublicationStatus

    @property
    def topic_id(self) -> TopicID:
        """Id топика."""
        return self._topic_id

    @property
    def name(self) -> str:
        """Название публикации."""
        return self._name

    @property
    def status(self) -> PublicationStatus:
        """Флаг верификации."""
        return self._status

    @BaseEntity.update
    def set_status(self, status: PublicationStatus):
        self._status = status

    @classmethod
    def register(
        cls,
        topic_id: TopicID,
        name: str,
        status: PublicationStatus = PublicationStatus.PENDING,
        id: PublicationID | None = None,
    ) -> Publication:
        now = datetime.now(UTC)
        return cls(
            _id=id or PublicationID.new(),
            _topic_id=topic_id,
            _name=name,
            _status=status,
            _created_at=now,
            _updated_at=now,
        )

    @classmethod
    def hydrate(
        cls,
        id: PublicationID,
        topic_id: TopicID,
        name: str,
        status: PublicationStatus,
        created_at: datetime,
        updated_at: datetime,
    ) -> Publication:
        return cls(
            _id=id or PublicationID.new(),
            _topic_id=topic_id,
            _name=name,
            _status=status,
            _created_at=created_at,
            _updated_at=updated_at,
        )
