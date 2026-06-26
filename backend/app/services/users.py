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


def create_pending_attorney(db: Session, full_name: str, email: str, password: str) -> User:
    user = User(
        full_name=full_name,
        email=email.lower(),
        password_hash=hash_password(password),
        role=UserRole.PENDING_ATTORNEY,
        is_active=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def ensure_bootstrap_admin(db: Session) -> None:
    settings = get_settings()
    email = str(settings.bootstrap_admin_email).lower()
    if get_user_by_email(db, email) is not None:
        return
    db.add(
        User(
            full_name="Bootstrap Admin",
            email=email,
            password_hash=hash_password(settings.bootstrap_admin_password),
            role=UserRole.ADMIN,
            is_active=True,
        )
    )
    db.commit()
