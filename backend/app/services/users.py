from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password, verify_password
from app.models.user import User, UserRole


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email.lower()))


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if user is None or not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def ensure_initial_attorney(db: Session) -> None:
    settings = get_settings()
    email = str(settings.internal_email).lower()
    if get_user_by_email(db, email) is not None:
        return
    db.add(
        User(
            email=email,
            password_hash=hash_password(settings.internal_password),
            role=UserRole.ATTORNEY,
            is_active=True,
        )
    )
    db.commit()
