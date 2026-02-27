from __future__ import annotations

from functools import lru_cache
from typing import Any

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    postgres_source_host: str = Field("postgres_source", env="POSTGRES_SOURCE_HOST")
    postgres_source_port: int = Field(5432, env="POSTGRES_SOURCE_PORT")
    postgres_source_db: str = Field("energy_source", env="POSTGRES_SOURCE_DB")
    postgres_source_user: str = Field("postgres", env="POSTGRES_SOURCE_USER")
    postgres_source_password: str = Field("postgres", env="POSTGRES_SOURCE_PASSWORD")

    postgres_target_host: str = Field("postgres_target", env="POSTGRES_TARGET_HOST")
    postgres_target_port: int = Field(5432, env="POSTGRES_TARGET_PORT")
    postgres_target_db: str = Field("energy_target", env="POSTGRES_TARGET_DB")
    postgres_target_user: str = Field("postgres", env="POSTGRES_TARGET_USER")
    postgres_target_password: str = Field("postgres", env="POSTGRES_TARGET_PASSWORD")

    api_host: str = Field("0.0.0.0", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


def build_source_db_url() -> str:
    settings = get_settings()
    return (
        f"postgresql+psycopg2://{settings.postgres_source_user}:"
        f"{settings.postgres_source_password}@"
        f"{settings.postgres_source_host}:{settings.postgres_source_port}/"
        f"{settings.postgres_source_db}"
    )


def build_target_db_url() -> str:
    settings = get_settings()
    return (
        f"postgresql+psycopg2://{settings.postgres_target_user}:"
        f"{settings.postgres_target_password}@"
        f"{settings.postgres_target_host}:{settings.postgres_target_port}/"
        f"{settings.postgres_target_db}"
    )

