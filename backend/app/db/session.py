from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from app.models.lead import Lead
    from app.models.user import User

    Base.metadata.create_all(bind=engine)
    _migrate_sqlite_schema()


def _migrate_sqlite_schema() -> None:
    if not settings.database_url.startswith("sqlite"):
        return

    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    with engine.begin() as connection:
        if "users" in table_names:
            user_columns = {column["name"] for column in inspector.get_columns("users")}
            if "full_name" not in user_columns:
                connection.execute(text("ALTER TABLE users ADD COLUMN full_name VARCHAR(160) NOT NULL DEFAULT 'Alma Attorney'"))
            if "last_assigned_at" not in user_columns:
                connection.execute(text("ALTER TABLE users ADD COLUMN last_assigned_at DATETIME"))

        if "leads" in table_names:
            lead_columns = {column["name"] for column in inspector.get_columns("leads")}
            if "assigned_attorney_id" not in lead_columns:
                connection.execute(text("ALTER TABLE leads ADD COLUMN assigned_attorney_id VARCHAR(36)"))
                connection.execute(text("CREATE INDEX IF NOT EXISTS ix_leads_assigned_attorney_id ON leads (assigned_attorney_id)"))
            if "assigned_attorney_email" not in lead_columns:
                connection.execute(text("ALTER TABLE leads ADD COLUMN assigned_attorney_email VARCHAR(255)"))
            if "assigned_at" not in lead_columns:
                connection.execute(text("ALTER TABLE leads ADD COLUMN assigned_at DATETIME"))
