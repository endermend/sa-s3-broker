from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, status
from pydantic import SecretStr

from sa_s3_broker.contexts.publication.application.dtos import (
    PublicationDTO,
    PublicationFiltersDTO,
    PublicationToDeleteDTO,
)
from sa_s3_broker.contexts.publication.application.use_cases.delete_publication import (
    DeletePublicationUseCase,
)
from sa_s3_broker.contexts.publication.application.use_cases.get_publications import (
    GetPublicationsUseCase,
)
from sa_s3_broker.contexts.publication.application.use_cases.post_publication import (
    PostPublicationUseCase,
)
from sa_s3_broker.presentation.api.schemas.publication import (
    CreatePublicationRequest,
    CreatePublicationResponce,
    PublicationsResponce,
)

router = APIRouter(prefix="/publication", tags=["Publication"])


@router.get(
    "/publications",
    status_code=status.HTTP_200_OK,
    summary="Получение списка файлов на скачивание.",
)
@inject
async def publications(
    use_case: FromDishka[GetPublicationsUseCase],
    topic_name: Annotated[
        str | None, Query(description="Название приватного топика")
    ] = None,
    password: Annotated[
        SecretStr | None, Query(description="Пароль от приватного топика")
    ] = None,
) -> list[PublicationsResponce]:
    output_dtos = await use_case.execute(
        input_dto=PublicationFiltersDTO(
            topic=topic_name,
            password=password.get_secret_value() if password is not None else None,
        )
    )
    return [
        PublicationsResponce(
            id=output_dto.id,
            topic=output_dto.topic,
            name=output_dto.name,
            status=output_dto.status,
            url=output_dto.url,
            expires_at=output_dto.expires_at,
        )
        for output_dto in output_dtos
    ]


@router.post(
    "/create_publication",
    status_code=status.HTTP_201_CREATED,
    summary="Создание публикации.",
)
@inject
async def create_publication(
    data: CreatePublicationRequest,
    use_case: FromDishka[PostPublicationUseCase],
) -> CreatePublicationResponce:
    output_dto = await use_case.execute(
        input_dto=PublicationDTO(
            topic=data.topic,
            name=data.name,
            password=data.password.get_secret_value(),
            status=data.status,
        ),
    )

    return CreatePublicationResponce(
        id=output_dto.id,
        url=output_dto.url,
        expires_at=output_dto.expires_at,
    )

@router.delete(
    "/delete_publication",
    status_code=status.HTTP_201_CREATED,
    summary="Удаление публикации.",
)
@inject
async def delete_publication(
    use_case: FromDishka[DeletePublicationUseCase],
    publication_id: Annotated[
        UUID, Query(description="Название приватного топика")
    ],
    password: Annotated[
        SecretStr, Query(description="Пароль от приватного топика")
    ],
) -> None:
    await use_case.execute(
        input_dto=PublicationToDeleteDTO(
            id=publication_id,
            password=password.get_secret_value(),
        )
    )