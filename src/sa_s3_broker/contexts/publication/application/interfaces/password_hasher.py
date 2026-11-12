from abc import abstractmethod
from typing import Protocol

from sa_s3_broker.contexts.publication.domain.value_objects.password_hash import (
    PasswordHash,
)


class IPasswordHasher(Protocol):
    """Протокол для хэширования паролей."""

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Хэширование пароля."""

    @abstractmethod
    def verify_password(self, password: str, password_hash: PasswordHash) -> bool:
        """Верификация пароля."""
