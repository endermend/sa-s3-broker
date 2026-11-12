import structlog
from pydantic import HttpUrl

from sa_s3_broker.contexts.publication.application.dtos import (
    PublicationFiltersDTO,
    PublicationViewDTO,
)
from sa_s3_broker.contexts.publication.application.exceptions import (
    InvalidCredentialsError,
)
from sa_s3_broker.contexts.publication.application.interfaces.bucket_service import (
    IBucketService,
)
from sa_s3_broker.contexts.publication.application.interfaces.password_hasher import (
    IPasswordHasher,
)
from sa_s3_broker.contexts.publication.domain.repositories.publication_repository import (
    IPublicationRepository,
)
from sa_s3_broker.contexts.publication.domain.repositories.topic_repository import (
    ITopicRepository,
)

logger = structlog.stdlib.get_logger()


class GetPublicationsUseCase:
    """Use case получения публикаций."""

    def __init__(
        self,
        topic_repo: ITopicRepository,
        publication_repo: IPublicationRepository,
        password_hasher: IPasswordHasher,
        bucket_service: IBucketService,
    ) -> None:
        """Инициализирует use case получение публикаций."""
        self._topic_repo = topic_repo
        self._publication_repo = publication_repo
        self._password_hasher = password_hasher
        self._bucket_service = bucket_service

    async def execute(
        self, input_dto: PublicationFiltersDTO
    ) -> list[PublicationViewDTO]:
        """
        Получает список публикаций для вывода с фильтром.

        Returns:
            список DTO с описанием публикаций

        Raises:
            InvalidCredentialsError: введен неверный пароль либо топика не существует

        """
        topic_id = None
        if input_dto.topic is not None:
            topic = await self._topic_repo.get_by_name(input_dto.topic)
            if topic is None:
                logger.warning("publ.topic.empty", reason="topic_no_exists")
                raise InvalidCredentialsError
            topic_id = topic.id
            if input_dto.password is None or not self._password_hasher.verify_password(
                input_dto.password, topic.password_hash
            ):
                logger.warning("publ.password.failed", reason="invalid_password")
                raise InvalidCredentialsError

        publications = await self._publication_repo.get_publications(
            topic_id, topic_id is not None
        )

        topics = [
            await self._topic_repo.get_by_id(pub.topic_id) for pub in publications
        ]

        links = [
            await self._bucket_service.presigned_get(pub)
            for pub in publications
        ]

        return [
            PublicationViewDTO(
                id=pub.id.value,
                topic=top.name if top is not None else "undefined",
                name=pub.name,
                status=pub.status.to_str(),
                url=HttpUrl(link[0]),
                expires_at=link[1],
            )
            for top, pub, link in zip(topics, publications, links, strict=True)
        ]
