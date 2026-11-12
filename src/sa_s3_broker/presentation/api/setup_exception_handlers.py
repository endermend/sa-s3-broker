from fastapi import FastAPI

from sa_s3_broker.presentation.api.exception_handlers import publication, shared


def setup_exception_handlers(app: FastAPI) -> None:
    """Установка обработчиков исключений по контекстам."""
    publication.setup_exception_handlers(app=app)
    shared.setup_exception_handlers(app=app)
