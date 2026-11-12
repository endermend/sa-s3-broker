from abc import abstractmethod
from datetime import timedelta
from typing import Protocol

from sa_s3_broker.contexts.publication.domain.entities.publication import Publication


class IBucketService(Protocol):
    """Сервис работы с бакетом."""

    @abstractmethod
    async def presigned_get(self, publication: Publication) -> tuple[str, timedelta]:
        """
        Создание подписанной ссылки на получение медиафайла.

        Returns:
            Ссылка на получение файла.
            Дата и время просрочевания ссылки.

        """

    @abstractmethod
    async def presigned_put(self, publication: Publication) -> tuple[str, timedelta]:
        """
        Создание подписанной ссылки на загрузку медиафайла.

        Returns:
            Ссылка на загрузку файла.
            Дата и время просрочевания ссылки.

        """

    @abstractmethod
    async def delete(self, publication: Publication) -> None:
        """Удаление файла по пути."""

    @abstractmethod
    async def check(self, publication: Publication) -> bool:
        """Проверка наличия файла в бакете."""
