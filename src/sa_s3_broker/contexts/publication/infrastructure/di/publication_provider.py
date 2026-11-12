from dishka import Provider

from sa_s3_broker.contexts.publication.infrastructure.di.db_provider import (
    PublicationDBProvider,
)
from sa_s3_broker.contexts.publication.infrastructure.di.password_hasher_provider import (
    PasswordHasherProvider,
)
from sa_s3_broker.contexts.publication.infrastructure.di.use_case_provider import (
    PublicationUseCaseProvider,
)
from src.sa_s3_broker.contexts.publication.infrastructure.di.bucket_service_provider import (
    BucketServiceProvider,
)


class PublicationProvider(
    PublicationDBProvider,
    PasswordHasherProvider,
    BucketServiceProvider,
    PublicationUseCaseProvider,
    Provider,
):
    """Провайдер, объединяющий провайдеры публикаций."""
