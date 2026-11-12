from dishka import (
    Provider,
    Scope,
    provide,
)

from sa_s3_broker.contexts.publication.application.interfaces.password_hasher import (
    IPasswordHasher,
)
from sa_s3_broker.contexts.publication.infrastructure.services.password_hasher import (
    ArgonPasswordHasher,
)


class PasswordHasherProvider(Provider):
    """Провайдер для PasswordHasher."""

    password_hasher = provide(
        ArgonPasswordHasher,
        scope=Scope.APP,
        provides=IPasswordHasher,
    )
