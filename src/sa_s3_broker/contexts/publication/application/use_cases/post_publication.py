from datetime import UTC, datetime, timedelta

import structlog
from arq import ArqRedis
from pydantic import HttpUrl

from sa_s3_broker.contexts.publication.application.dtos import LinkDTO, PublicationDTO
from sa_s3_broker.contexts.publication.application.exceptions import (
    InvalidCredentialsError,
)
from sa_s3_broker.contexts.publication.application.interfaces.bucket_service import (
    IBucketService,
)
from sa_s3_broker.contexts.publication.application.interfaces.password_hasher import (
    IPasswordHasher,
)
from sa_s3_broker.contexts.publication.domain.entities.publication import (
    Publication,
)
from sa_s3_broker.contexts.publication.domain.entities.topic import Topic
from sa_s3_broker.contexts.publication.domain.repositories.publication_repository import (
    IPublicationRepository,
)
from sa_s3_broker.contexts.publication.domain.repositories.topic_repository import (
    ITopicRepository,
)
from sa_s3_broker.contexts.publication.domain.value_objects.password_hash import (
    PasswordHash,
)
from sa_s3_broker.contexts.publication.domain.value_objects.publication_status import (
    PublicationStatus,
)

logger = structlog.stdlib.get_logger()


class PostPublicationUseCase:
    """Use case создания публикации."""

    def __init__(
        self,
        topic_repo: ITopicRepository,
        publication_repo: IPublicationRepository,
        password_hasher: IPasswordHasher,
        bucket_service: IBucketService,
        arq_pool: ArqRedis,
    ) -> None:
        """Инициализирует use case публикации медиафайла в топике."""
        self._topic_repo = topic_repo
        self._publication_repo = publication_repo
        self._password_hasher = password_hasher
        self._bucket_service = bucket_service
        self._arq_pool = arq_pool

    async def execute(self, input_dto: PublicationDTO) -> LinkDTO:
        """
        Создает публикацию и дает подписанную ссылку на загрузку медиафайла.

        Returns:
            DTO с подписанной ссылкой.

        Raises:
            InvalidCredentialsError: введен неверный пароль

        """
        topic = await self._topic_repo.get_by_name(input_dto.topic)
        if topic is None:
            topic = Topic.register(
                name = input_dto.topic,
                password_hash=PasswordHash(self._password_hasher.hash_password(input_dto.password)),
            )
            await self._topic_repo.save(topic)

        if not self._password_hasher.verify_password(input_dto.password, topic.password_hash):
            logger.warning("publ.password.failed", reason="invalid_password")
            raise InvalidCredentialsError

        publication = Publication.register(
            topic_id=topic.id,
            name=input_dto.name,
            status=PublicationStatus.PENDING,
        )
        await self._publication_repo.save(publication)

        url_link, expires_in = await self._bucket_service.presigned_put(publication)

        await self._arq_pool.enqueue_job(
            "check_expiration_task",
            publication.id.value,
            PublicationStatus(input_dto.status) == PublicationStatus.PUBLIC,
            _defer_by=expires_in + timedelta(minutes=1),
        )

        return LinkDTO(
            id = publication.id.value,
            url = HttpUrl(url_link),
            expires_at = datetime.now(UTC) + expires_in,
        )
