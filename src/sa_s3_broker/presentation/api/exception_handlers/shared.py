import structlog
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from sa_s3_broker.shared.domain.exceptions import DomainError

logger = structlog.stdlib.get_logger()

def base_domain_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Хэндлер базовой ошибки домена.

    Returns:
        JSONResponse

    """
    logger.exception('domain.error')
    return JSONResponse(
        content={"detail": "Unprocessable domain error id."},
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """Установка обработчиков ошибок."""
    app.add_exception_handler(DomainError, base_domain_handler)
