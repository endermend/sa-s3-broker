from abc import abstractmethod
from typing import Protocol

from sa_s3_broker.contexts.publication.domain.entities.publication import Publication
from sa_s3_broker.contexts.publication.domain.value_objects.publication_id import (
    PublicationID,
)
from sa_s3_broker.contexts.publication.domain.value_objects.topic_id import TopicID


class IPublicationRepository(Protocol):
    """Репозиторий для работы с публикациями."""

    @abstractmethod
    async def save(self, publication: Publication) -> None:
        """Сохранение публикации."""

    @abstractmethod
    async def get_by_id(self, publication_id: PublicationID) -> Publication | None:
        """
        Получение публикации по id.
        
        Returns:
            Publication или None, если публикации с таким ID нет.
        
        """

    @abstractmethod
    async def get_publications(self, topic_id: TopicID | None = None, get_private: bool = False) -> list[Publication]:
        """
        Получение списка публикаций: публичных или приватных по топику.
        
        Returns:
            Список публикаций.
        
        """

    @abstractmethod
    async def delete_publication(self, publication_id: PublicationID) -> bool:
        """
        Удаление записи публикации.

        Returns:
            True, если запись была удалена.

        """