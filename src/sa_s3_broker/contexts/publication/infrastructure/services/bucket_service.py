from datetime import UTC, datetime, timedelta
from typing import override

from botocore.exceptions import ClientError
from mypy_boto3_s3 import S3Client

from sa_s3_broker.contexts.publication.application.interfaces.bucket_service import (
    IBucketService,
)
from sa_s3_broker.contexts.publication.domain.entities.publication import Publication
from sa_s3_broker.infrastructure.config import Config
from sa_s3_broker.shared.domain.exceptions import DomainError


class BucketService(IBucketService):
    """Сервис работы с бакетом через cloud.ru."""

    def __init__(self, s3_client: S3Client, config: Config) -> None:
        """Инициализация BucketService."""
        self._client = s3_client
        self._config = config

    @staticmethod
    def _publication_path(publication: Publication) -> str:
        return f"topics/{publication.topic_id.value}/{publication.id.value}"

    @override
    async def presigned_get(self, publication: Publication) -> tuple[str, datetime]:
        presigned_get_url = self._client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": self._config.S3.BUCKET_NAME,
                "Key": self._publication_path(publication),
            },
            ExpiresIn=self._config.S3.LIFESPAN + 30,
        )
        return presigned_get_url, datetime.now(UTC) + timedelta(seconds=self._config.S3.LIFESPAN)

    @override
    async def presigned_put(self, publication: Publication) -> tuple[str, datetime]:
        presigned_get_url = self._client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self._config.S3.BUCKET_NAME,
                "Key": self._publication_path(publication),
            },
            ExpiresIn=self._config.S3.LIFESPAN + 30,
        )
        return presigned_get_url, datetime.now(UTC) + timedelta(seconds=self._config.S3.LIFESPAN)

    @override
    async def delete(self, publication: Publication) -> None:
        self._client.delete_object(
            Bucket=self._config.S3.BUCKET_NAME,
            Key=self._publication_path(publication),
        )

    @override
    async def check(self, publication: Publication) -> bool:
        try:
            self._client.head_object(
                Bucket=self._config.S3.BUCKET_NAME,
                Key=self._publication_path(publication),
            )
            return True
        except ClientError as e:
            code = e.response.get("Error", {}).get("Code")
            if code in ("404", "NoSuchKey", "NotFound"):
                return False
            raise DomainError
