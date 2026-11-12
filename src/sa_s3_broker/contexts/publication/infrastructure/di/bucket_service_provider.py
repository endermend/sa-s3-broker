import boto3
from botocore.client import Config as CF
from dishka import (
    Provider,
    Scope,
    provide,
)
from mypy_boto3_s3 import S3Client

from sa_s3_broker.contexts.publication.application.interfaces.bucket_service import (
    IBucketService,
)
from sa_s3_broker.contexts.publication.infrastructure.services.bucket_service import (
    BucketService,
)
from sa_s3_broker.infrastructure.config import Config


class BucketServiceProvider(Provider):
    """Провайдер для BucketService."""

    @provide(scope=Scope.APP)
    @staticmethod
    def get_s3_client(config: Config) -> S3Client:
        """
        Провайдер для клиента Cloud.ru.

        Returns:
            S3Client

        """
        s3_config = CF(
            region_name="ru-central-1",
            signature_version="s3v4",
            s3={"addressing_style": "path"},
        )

        print(f"AK: {config.S3.AWS_ACCESS_KEY!r}")
        print(f"SK length: {len(config.S3.SECRET_KEY)}")
        print(f"Endpoint: {config.S3.ENDPOINT}")

        return boto3.client(
            "s3",
            endpoint_url=config.S3.ENDPOINT,
            aws_access_key_id=config.S3.AWS_ACCESS_KEY,
            aws_secret_access_key=config.S3.SECRET_KEY,
            config=s3_config,
            region_name="ru-central-1",
        )

    bucket_provider = provide(
        BucketService,
        scope=Scope.APP,
        provides=IBucketService,
    )
