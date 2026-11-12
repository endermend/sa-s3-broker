from abc import abstractmethod
from typing import Protocol

from sa_s3_broker.contexts.publication.domain.entities.topic import Topic
from sa_s3_broker.contexts.publication.domain.value_objects.topic_id import TopicID


class ITopicRepository(Protocol):

    @abstractmethod
    async def save(self, topic: Topic) -> None:
        """Сохранение топика."""

    async def get_by_id(self, topic_id: TopicID) -> Topic | None:
        """
        Получение топика по id.

        Returns:
            Топик или None, если топика с таким id нет.

        """

    async def get_by_name(self, topic_name: str) -> Topic | None:
        """
        Получение топика по названию.

        Returns:
            Топик или None, если топика с таким названием нет.

        """