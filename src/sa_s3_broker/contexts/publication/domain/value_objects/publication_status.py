from enum import IntEnum
from typing import cast

from sa_s3_broker.contexts.publication.domain.types import PublicationStatusType
from sa_s3_broker.shared.domain.exceptions import DomainError


class PublicationStatus(IntEnum):
    """Value object статуса пользователя."""

    PENDING = 0
    PUBLIC = 1
    PRIVATE = 2

    def to_str(self) -> PublicationStatusType:
        return cast("PublicationStatusType", self.name.lower())

    @classmethod
    def from_str(cls, value: str) -> PublicationStatus:
        try:
            return cls[value.upper()]
        except KeyError:
            raise DomainError(f"Invalid PublicationStatus string: {value}")