from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from sa_s3_broker.shared.infrastructure.models.base_model import Base


class TopicORMModel(Base):
    """ORM Модель топика."""

    __tablename__ = "topics"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<TopicModel(id={self.id}, name={self.name})>"
