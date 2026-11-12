from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from sa_s3_broker.contexts.publication.infrastructure.di.publication_provider import (
    PublicationProvider,
)
from sa_s3_broker.infrastructure.config import Config
from sa_s3_broker.shared.infrastructure.di.providers import DBProvider, RQProvider


def make_container_di(config: Config) -> AsyncContainer:
    """
    Создание асинхронного контейнера.

    Returns:
        AsyncContainer

    """
    return make_async_container(
        DBProvider(),
        RQProvider(),
        PublicationProvider(),
        FastapiProvider(),
        context={Config: config},
    )
