from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, HttpUrl, SecretStr


class PublicationsResponce(BaseModel):
    id: UUID
    topic: str
    name: str
    status: str
    url: HttpUrl
    expires_at: datetime

class CreatePublicationRequest(BaseModel):
    topic: str
    name: str
    password: SecretStr
    status: Literal["public", "private"]

class CreatePublicationResponce(BaseModel):
    """DTO ссылки на загрузку/скачивание."""

    id: UUID
    url: HttpUrl
    expires_at: datetime