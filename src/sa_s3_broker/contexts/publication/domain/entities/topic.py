from dataclasses import dataclass
from datetime import UTC, datetime

from sa_s3_broker.contexts.publication.domain.value_objects.password_hash import (
    PasswordHash,
)
from sa_s3_broker.contexts.publication.domain.value_objects.topic_id import TopicID
from sa_s3_broker.shared.domain.base_entity import BaseEntity


@dataclass(slots=True)
class Topic(BaseEntity[TopicID]):
    """Доменная сущность публикации (Entity DDD)."""

    _name: str
    _password_hash: PasswordHash

    @property
    def name(self) -> str:
        """Название топика."""
        return self._name

    @property
    def password_hash(self) -> PasswordHash:
        """Флаг верификации."""
        return self._password_hash

    @classmethod
    def register(
        cls,
        name: str,
        password_hash: PasswordHash,
        id: TopicID | None = None,
    ) -> Topic:
        now = datetime.now(UTC)
        return cls(
            _id=id or TopicID.new(),
            _password_hash=password_hash,
            _name=name,
            _created_at=now,
            _updated_at=now,
        )

    @classmethod
    def hydrate(
        cls,
        id: TopicID,
        name: str,
        password_hash: PasswordHash,
        created_at: datetime,
        updated_at: datetime,
    ) -> Topic:
        return cls(
            _id=id,
            _name=name,
            _password_hash=password_hash,
            _created_at=created_at,
            _updated_at=updated_at,
        )
