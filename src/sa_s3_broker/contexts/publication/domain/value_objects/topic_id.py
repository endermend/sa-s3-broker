from uuid import UUID

from sa_s3_broker.shared.domain.value_objects.base_id import BaseID


class TopicID(BaseID):
    """Value object ID топика."""

    value: UUID
