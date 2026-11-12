from abc import ABC, abstractmethod
from typing import Any


class BaseValueObject(ABC):
    """Базовый класс для Value Objects."""

    @abstractmethod
    def _get_equality_components(self) -> tuple[Any, ...]:
        """
        Определение равенства двух VO.

        Returns:
            Кортеж, определяющий равенство.

        """

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._get_equality_components() == other._get_equality_components()

    def __hash__(self) -> int:
        def make_hashable(obj: object) -> object:
            if isinstance(obj, (list, set)):
                # Convert list/set to tuple, recursively handling nested structures
                return tuple(make_hashable(item) for item in obj)
            if isinstance(obj, dict):
                # Convert dict to tuple of sorted items
                return tuple(
                    (make_hashable(k), make_hashable(v)) for k, v in sorted(obj.items())
                )
            return obj

        objects = tuple(make_hashable(obj) for obj in self._get_equality_components())
        return hash(tuple(objects))

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        components = self._get_equality_components()
        return ", ".join(repr(c) for c in components)
