import uuid
from datetime import UTC, datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def _utc_now() -> datetime:
    """
    Текущее время по UTC.

    Returns:
        Текущее время по UTC.

    """
    return datetime.now(UTC)


class Base(AsyncAttrs, DeclarativeBase):
    """Базовая модель sqlalchemy."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=_utc_now,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=_utc_now,
        onupdate=_utc_now,
        nullable=False,
    )

    version: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        nullable=False,
    )
