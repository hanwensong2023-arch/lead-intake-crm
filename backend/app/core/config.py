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
    extra_cors_origins: str = "http://127.0.0.1:3000,http://localhost:3001,http://127.0.0.1:3001"
    upload_dir: Path = Path("./data/uploads")
    outbox_dir: Path = Path("./data/outbox")
    max_resume_bytes: int = 5 * 1024 * 1024
    allowed_resume_types: set[str] = {
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    bootstrap_admin_email: EmailStr = "admin@example.com"
    bootstrap_admin_password: str = "change-me-admin"
    auth_secret: str = "dev-only-change-me"
    access_token_minutes: int = 8 * 60

    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_from_email: EmailStr = "noreply@example.com"
    smtp_use_tls: bool = True
    mailtrap_api_url: str = "https://send.api.mailtrap.io/api/send"
    mailtrap_api_token: str | None = None
    mailtrap_from_email: EmailStr = "hello@demomailtrap.co"
    mailtrap_from_name: str = "Alma"
    mailtrap_use_sandbox: bool = False
    mailtrap_inbox_id: int | None = None
    mailtrap_send_delay_seconds: float = 6.0

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
