from uuid import UUID

from sa_s3_broker.shared.domain.value_objects.base_id import BaseID


class PublicationID(BaseID):
    """Value object ID публикации."""

    value: UUID
