from typing import override

from argon2 import PasswordHasher as Argon2PasswordHasher
from argon2.exceptions import VerifyMismatchError

from sa_s3_broker.contexts.publication.application.interfaces.password_hasher import (
    IPasswordHasher,
)
from sa_s3_broker.contexts.publication.domain.value_objects.password_hash import (
    PasswordHash,
)


class ArgonPasswordHasher(IPasswordHasher):
    """Реализация IPasswordHasher на Argon2."""

    def __init__(self) -> None:
        """Инициализация PasswordHasher."""
        self._ph = Argon2PasswordHasher()

    @override
    def hash_password(self, password: str) -> str:
        """
        Хэширование пароля.

        Returns:
            str

        """
        return self._ph.hash(password=password)

    @override
    def verify_password(self, password: str, password_hash: PasswordHash) -> bool:
        """
        Верификация пароля.

        Returns:
            bool: True если прошел верификацию, False иначе

        """
        try:
            self._ph.verify(hash=password_hash.value, password=password)
        except VerifyMismatchError:
            return False
        return True
