from dishka import (
    Provider,
    Scope,
    provide,  # pyright: ignore[reportUnknownVariableType]
)

from sa_s3_broker.contexts.publication.application.use_cases.delete_publication import (
    DeletePublicationUseCase,
)
from sa_s3_broker.contexts.publication.application.use_cases.get_publications import (
    GetPublicationsUseCase,
)
from sa_s3_broker.contexts.publication.application.use_cases.post_publication import (
    PostPublicationUseCase,
)


class PublicationUseCaseProvider(Provider):
    """Провайдер для всей Publication UseCase."""

    scope = Scope.REQUEST

    post_publ = provide(PostPublicationUseCase)
    get_publs = provide(GetPublicationsUseCase)
    del_pub = provide(DeletePublicationUseCase)
