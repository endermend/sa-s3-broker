import asyncio
from uuid import UUID

from dishka import FromDishka
from dishka_rq import inject

from sa_s3_broker.contexts.publication.application.interfaces.bucket_service import (
    IBucketService,
)
from sa_s3_broker.contexts.publication.domain.repositories.publication_repository import (
    IPublicationRepository,
)
from sa_s3_broker.contexts.publication.domain.value_objects.publication_id import (
    PublicationID,
)
from sa_s3_broker.contexts.publication.domain.value_objects.publication_status import (
    PublicationStatus,
)


@inject
def check_expiration_task(
    publication_id_value: UUID,
    is_public: bool,
    publication_repo: FromDishka[IPublicationRepository],
    bucket: FromDishka[IBucketService],
) -> None:
    asyncio.run(
        _check_expiration_async(
            publication_id_value, is_public, publication_repo, bucket
        )
    )


async def _check_expiration_async(
    publication_id_value: UUID,
    is_public: bool,
    publication_repo: FromDishka[IPublicationRepository],
    bucket: FromDishka[IBucketService],
):
    publication_id = PublicationID(publication_id_value)
    publication = await publication_repo.get_by_id(publication_id)
    if publication is None or publication.status != PublicationStatus.PENDING:
        return
    if await bucket.check(publication):
        publication.set_status(
            PublicationStatus.PUBLIC if is_public else PublicationStatus.PRIVATE
        )
        await publication_repo.save(publication)
    else:
        await publication_repo.delete_publication(publication.id)
