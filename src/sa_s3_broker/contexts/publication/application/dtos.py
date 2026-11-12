from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class PublicationDTO(BaseModel):
    """DTO публикации."""

    topic: str
    name: str
    password: str
    status: Literal["public", "private"]


class PublicationViewDTO(BaseModel):
    """DTO публикации для просмотра."""

    id: UUID
    topic: str
    name: str
    status: str
    url: HttpUrl
    expires_at: datetime


class PublicationToDeleteDTO(BaseModel):
    """DTO публикации для удаления."""

    id: UUID
    password: str


class PublicationFiltersDTO(BaseModel):
    """Фильтр публикаций."""

    topic: str | None
    password: str | None


class LinkDTO(BaseModel):
    """DTO ссылки на загрузку/скачивание."""

    id: UUID
    url: HttpUrl
    expires_at: datetime
