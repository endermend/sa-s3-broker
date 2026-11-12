import uvicorn

from sa_s3_broker.infrastructure.config import Config
from sa_s3_broker.infrastructure.log_config import setup_logging


def main() -> None:
    """Запуск FastAPI приложения в помощью uvicorn."""
    config = Config()  # type:ignore[call-arg]
    setup_logging(env=config.APP.ENV)

    uvicorn.run(
        "sa_s3_broker.presentation.api.app_factory:create_app",
        factory=True,
        host="0.0.0.0",
        port=config.APP.PORT,
        log_config=None,
        access_log=config.APP.ENV == "dev",
    )


if __name__ == "__main__":
    main()
