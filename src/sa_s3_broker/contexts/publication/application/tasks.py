from uuid import UUID

import structlog
from dishka.integrations.arq import FromDishka, inject

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

logger = structlog.stdlib.get_logger()

@inject
async def check_expiration_task(
    ctx: dict,
    publication_id_value: UUID,
    is_public: bool,
    publication_repo: FromDishka[IPublicationRepository],
    bucket: FromDishka[IBucketService],
) -> None:
    publication_id = PublicationID(publication_id_value)
    publication = await publication_repo.get_by_id(publication_id)
    
    if publication is None or publication.status != PublicationStatus.PENDING:
        return
        
    logger.info("task.started", publication_id=publication_id_value, created_at=publication.created_at)

    did_saved = await bucket.check(publication)
    
    if did_saved:
        publication.set_status(
            PublicationStatus.PUBLIC if is_public else PublicationStatus.PRIVATE
        )
        await publication_repo.save(publication)
    elif not await publication_repo.delete_publication(publication.id):
        logger.error("task.failed", reason="publication has not been deleted.")
        return
        
    logger.info("task.finished", publication_id=publication_id_value, did_saved=did_saved)