from typing import Any, Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DB(BaseModel):
    """Конфиг базы данных."""

    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str

class REDIS(BaseModel):
    """Конфиг redis."""

    HOST: str
    PORT: int
    PASSWORD: str

class S3(BaseModel):
    """Конфиг базы данных."""

    ENDPOINT: str
    GLOBAL_ENDPOINT: str
    TENANT_ID: str
    ACCESS_KEY: str
    SECRET_KEY: str
    BUCKET_NAME: str
    LIFESPAN: int

    AWS_ACCESS_KEY: str = Field(default="", init=False)

    def model_post_init(self, context: Any, /) -> None:
        self.AWS_ACCESS_KEY = f"{self.TENANT_ID}.{self.ACCESS_KEY}"


class APP(BaseModel):
    """Конфиг приложения."""

    PORT: int
    ENV: Literal["dev", "prod"]


class Config(BaseSettings):
    """Конфиг всех конфигов."""

    S3: S3
    DB: DB
    REDIS: REDIS
    APP: APP

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        extra="ignore",
    )
