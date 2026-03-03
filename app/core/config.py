"""Application configuration."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SmartFlow Enterprise"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./smartflow.db"
    secret_key: str = "change-me-secret"
    access_token_minutes: int = 15
    refresh_token_days: int = 7
    redis_url: str = "redis://redis:6379/0"
    openai_api_key: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
