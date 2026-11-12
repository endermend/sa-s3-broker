import structlog

from sa_s3_broker.contexts.publication.application.dtos import (
    PublicationToDeleteDTO,
)
from sa_s3_broker.contexts.publication.application.exceptions import (
    InvalidCredentialsError,
    InvalidPublicationError,
    InvalidTopicError,
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
from sa_s3_broker.contexts.publication.domain.value_objects.publication_id import (
    PublicationID,
)

logger = structlog.stdlib.get_logger()


class DeletePublicationUseCase:
    """Use case удаления публикации."""

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

    async def execute(self, input_dto: PublicationToDeleteDTO) -> None:
        """
        Получает список публикаций для вывода с фильтром.

        Returns:
            список DTO с описанием публикаций

        Raises:
            InvalidTopicError: топика не существует
            InvalidPublicationError: публикации не существует
            InvalidCredentialsError: введен неверный пароль

        """
        publication_id = PublicationID(input_dto.id)
        publication = await self._publication_repo.get_by_id(publication_id)

        if publication is None:
            logger.warning("publ.publid.failed", reason="publication_no_exists")
            raise InvalidPublicationError

        topic = await self._topic_repo.get_by_id(publication.topic_id)
        if topic is None:
            logger.warning("publ.topicid.failed", reason="topic_no_exists")
            raise InvalidTopicError

        if input_dto.password is None or not self._password_hasher.verify_password(
            input_dto.password, topic.password_hash
        ):
            logger.warning("publ.password.failed", reason="invalid_password")
            raise InvalidCredentialsError

        await self._bucket_service.delete(publication)
        await self._publication_repo.delete_publication(publication.id)
