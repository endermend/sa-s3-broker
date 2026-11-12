from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from sa_s3_broker.contexts.publication.application.exceptions import (
    ApplicationError,
    InvalidCredentialsError,
    InvalidPublicationError,
    InvalidTopicError,
)


def application_handler(request: Request, exc: Exception, /) -> JSONResponse:
    """
    Хэндлер ошибки с неверным логином или паролем.

    Returns:
        JSONResponse

    """
    return JSONResponse(
        content={"detail": "Some shit happened"},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


def invalid_publication_handler(request: Request, exc: Exception, /) -> JSONResponse:
    """
    Хэндлер ошибки с неверным логином или паролем.

    Returns:
        JSONResponse

    """
    return JSONResponse(
        content={"detail": "Publication does not exists"},
        status_code=status.HTTP_404_NOT_FOUND,
    )


def invalid_topic_handler(request: Request, exc: Exception, /) -> JSONResponse:
    """
    Хэндлер ошибки с неверным логином или паролем.

    Returns:
        JSONResponse

    """
    return JSONResponse(
        content={"detail": "Topic does not exists"},
        status_code=status.HTTP_404_NOT_FOUND,
    )


def invalid_credentials_handler(request: Request, exc: Exception, /) -> JSONResponse:
    """
    Хэндлер ошибки с неверным логином или паролем.

    Returns:
        JSONResponse

    """
    return JSONResponse(
        content={"detail": "Invalid topic or password"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """Подключение хэндлеров ошибок."""
    app.add_exception_handler(ApplicationError, application_handler)
    app.add_exception_handler(InvalidCredentialsError, invalid_credentials_handler)
    app.add_exception_handler(InvalidPublicationError, invalid_publication_handler)
    app.add_exception_handler(InvalidTopicError, invalid_topic_handler)
