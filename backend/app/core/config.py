from functools import lru_cache
from pathlib import Path

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Lead Intake CRM"
    environment: str = "local"
    database_url: str = "sqlite:///./data/leads.db"
    frontend_origin: str = "http://localhost:3000"
    extra_cors_origins: str = "http://127.0.0.1:3000"
    upload_dir: Path = Path("./data/uploads")
    outbox_dir: Path = Path("./data/outbox")
    max_resume_bytes: int = 5 * 1024 * 1024
    allowed_resume_types: set[str] = {
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    internal_email: EmailStr = "attorney@example.com"
    internal_password: str = "change-me"
    auth_secret: str = "dev-only-change-me"
    access_token_minutes: int = 8 * 60

    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_from_email: EmailStr = "noreply@example.com"
    smtp_use_tls: bool = True

    @property
    def cors_origins(self) -> list[str]:
        origins = [self.frontend_origin]
        origins.extend(origin.strip() for origin in self.extra_cors_origins.split(",") if origin.strip())
        return list(dict.fromkeys(origins))


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.outbox_dir.mkdir(parents=True, exist_ok=True)
    Path("./data").mkdir(parents=True, exist_ok=True)
    return settings
