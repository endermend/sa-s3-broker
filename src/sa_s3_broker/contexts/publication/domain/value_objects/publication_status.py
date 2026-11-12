from typing import ClassVar

from sa_s3_broker.contexts.publication.domain.types import PublicationStatusType
from sa_s3_broker.shared.domain.exceptions import DomainError
from sa_s3_broker.shared.domain.value_objects.single_value_object import (
    SingleValueObject,
)


class PublicationStatus(SingleValueObject):
    """Value object статуса пользователя."""

    value: int

    PENDING: ClassVar[PublicationStatus]
    PUBLIC: ClassVar[PublicationStatus]
    PRIVATE: ClassVar[PublicationStatus]

    def to_str(self) -> PublicationStatusType:
        """
        Преобразует в строку.

        Returns:
            UserStatusType

        Raises:
            DomainError: если не смог преобразовать

        """
        if self.value == PublicationStatus.PENDING.value:
            return "pending"
        if self.value == PublicationStatus.PUBLIC.value:
            return "public"
        if self.value == PublicationStatus.PRIVATE.value:
            return "private"
        raise DomainError

    def to_val(self) -> int:
        """
        Преобразует в число.

        Returns:
            UserStatusType

        Raises:
            DomainError: если не смог преобразовать

        """
        if self.value == PublicationStatus.PENDING.value:
            return 0
        if self.value == PublicationStatus.PUBLIC.value:
            return 1
        if self.value == PublicationStatus.PRIVATE.value:
            return 2
        raise DomainError

    @classmethod
    def from_val(cls, value: int) -> PublicationStatus:
        """
        Преобразует в число.

        Returns:
            UserStatusType

        Raises:
            DomainError: если не смог преобразовать

        """
        if value == 0:
            return PublicationStatus.PENDING;
        if value == 1:
            return PublicationStatus.PUBLIC
        if value == 2:
            return PublicationStatus.PRIVATE
        raise DomainError


PublicationStatus.PENDING = PublicationStatus(0)
PublicationStatus.PUBLIC = PublicationStatus(1)
PublicationStatus.PRIVATE = PublicationStatus(2)
