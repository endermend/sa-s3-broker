from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sa_s3_broker.presentation.api.middleware.logging_middleware import (
    LoggingMiddleware,
)


def setup_middleware(app: FastAPI) -> None:
    """Подключение Middleware к FastAPI."""
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
