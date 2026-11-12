from dataclasses import dataclass
from typing import Any, override

from sa_s3_broker.shared.domain.value_objects.base_value_object import BaseValueObject


@dataclass(slots=True, frozen=True)
class SingleValueObject(BaseValueObject):
    """Базовый Single Value Object."""

    value: Any

    @override
    def _get_equality_components(self) -> tuple[Any, ...]:
        return (self.value,)
