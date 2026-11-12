from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TypeVar

from sa_s3_broker.shared.domain.value_objects.base_id import BaseID

R = TypeVar("R")

@dataclass(slots=True)
class BaseEntity[ID: BaseID]:
    """Базовый класс доменной сущности."""

    _id: ID
    _created_at: datetime
    _updated_at: datetime

    @property
    def id(self) -> ID:
        """Id сущности."""
        return self._id

    @property
    def created_at(self) -> datetime:
        """Дата создания сущности."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Дата обновления сущности."""
        return self._updated_at

    @staticmethod
    def update(
        func: Callable[..., R],
    ) -> Callable[..., R]:
        """Декоратор для обновления временной метки обновления сущности."""

        def wrapper(self: BaseEntity, *args: object | None, **kwargs: object | None) -> R:
            result = func(self, *args, **kwargs)

            self._updated_at = datetime.now(UTC)
            return result

        return wrapper

    def __eq__(self, value: object) -> bool:
        """
        Сущности сравниваются по идентичности (DDD).

        Returns:
            Результат сравнения по self.id

        """
        if not isinstance(value, BaseEntity):
            return NotImplemented
        return self._id == value._id

    def __hash__(self) -> int:
        """
        Сущности хэшируются по идентичности (DDD).

        Returns:
            Хеш по self.id

        """
        return hash(self._id)
