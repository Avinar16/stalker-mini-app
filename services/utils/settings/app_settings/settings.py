# settings.py
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "stalker_kombat"
    ECHO_SQL: bool = False
    BOT_TOKEN: str
    ALLOWED_ORIGINS: str

    @property
    def database_url_sync(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def database_url_async(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
