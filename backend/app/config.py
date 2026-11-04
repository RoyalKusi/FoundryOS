"""App config via pydantic-settings. All secrets via env, never hard-coded."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_env: Literal["local", "staging", "prod", "test"] = Field(default="local")
    app_secret_key: str = Field(default="change-me-in-prod", alias="APP_SECRET_KEY")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:54322/postgres",
        alias="DATABASE_URL",
    )
    supabase_url: str = Field(default="http://localhost:54321", alias="SUPABASE_URL")
    supabase_service_key: str = Field(default="test-service-key", alias="SUPABASE_SERVICE_KEY")
    supabase_anon_key: str = Field(default="test-anon-key", alias="SUPABASE_ANON_KEY")

    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    baseten_api_key: str = Field(default="", alias="BASETEN_API_KEY")
    baseten_base_url: str = Field(
        default="https://inference.baseten.co/v1", alias="BASETEN_BASE_URL"
    )
    baseten_reasoning_model: str = Field(
        default="meta-llama/Llama-4-Maverick-17B-128E-Instruct",
        alias="BASETEN_REASONING_MODEL",
    )
    baseten_fast_model: str = Field(
        default="meta-llama/Llama-4-Scout-17B-16E-Instruct",
        alias="BASETEN_FAST_MODEL",
    )
    baseten_embedding_url: str = Field(default="", alias="BASETEN_EMBEDDING_URL")
    baseten_reranker_url: str = Field(default="", alias="BASETEN_RERANKER_URL")
    baseten_whisper_url: str = Field(default="", alias="BASETEN_WHISPER_URL")

    llm_mode: Literal["mock", "live"] = Field(default="mock", alias="LLM_MODE")
    token_budget_monthly: int = Field(default=1_000_000, alias="TOKEN_BUDGET_MONTHLY")

    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:8080"]
    )

    # Token accounting
    max_tool_calls_per_run: int = 8
    max_wall_time_seconds: int = 120
    max_steps_per_plan: int = 5


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
