from typing import Self
from uuid import UUID, uuid4

from sa_s3_broker.shared.domain.value_objects.single_value_object import (
    SingleValueObject,
)


class BaseID(SingleValueObject):
    """Базовый value object ID."""

    value: UUID

    @classmethod
    def new(cls) -> Self:
        """
        Генерация нового ID.

        Returns:
            ID

        """
        return cls(uuid4())

    @classmethod
    def from_str(cls, uuid_str: str) -> Self:
        """
        Получение ID из строки str.

        Returns:
            ID

        """
        return cls(UUID(uuid_str))
