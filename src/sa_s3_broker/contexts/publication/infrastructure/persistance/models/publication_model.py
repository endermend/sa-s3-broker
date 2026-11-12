import uuid

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from sa_s3_broker.shared.infrastructure.models.base_model import Base


class PublicationORMModel(Base):
    """ORM Модель публкации."""

    __tablename__ = "publications"

    topic_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"<PublModel(id={self.id}, name={self.name}, topic={self.topic_id})>"
