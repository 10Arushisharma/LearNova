from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "Learnova"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "learnova-dev-secret-key-change-in-production-64chars-minimum"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14
    PASSWORD_RESET_EXPIRE_MINUTES: int = 30

    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"

    # Database: PostgreSQL primary; SQLite supported seamlessly for local standalone/test runs
    DATABASE_URL: str = "sqlite:///./learnova_dev.db"

    # Redis / Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    CELERY_TASK_ALWAYS_EAGER: bool = True

    # OpenAI-compatible AI Mentor Provider
    AI_PROVIDER: str = "openai_compatible"
    AI_BASE_URL: str = "https://api.openai.com/v1"
    AI_API_KEY: str = ""
    AI_MODEL: str = "gpt-4o-mini"
    AI_MAX_TOKENS: int = 900
    AI_TEMPERATURE: float = 0.4

    # Sandboxed Python Execution
    SANDBOX_MODE: str = "subprocess"  # "docker" in compose/prod, "subprocess" in local dev
    SANDBOX_IMAGE: str = "learnova-python-sandbox:latest"
    SANDBOX_TIMEOUT_SECONDS: int = 5
    SANDBOX_MEMORY_LIMIT: str = "128m"
    SANDBOX_CPU_LIMIT: str = "0.5"

    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 120
    MENTOR_RATE_LIMIT_PER_MINUTE: int = 20
    SANDBOX_RATE_LIMIT_PER_MINUTE: int = 30


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
