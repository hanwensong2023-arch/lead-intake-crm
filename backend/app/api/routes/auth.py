from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from sqlalchemy import select

from app.api.deps import require_admin_user, require_internal_user
from app.core.security import create_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.auth import AttorneyListResponse, AttorneyRead, AuthUser, LoginRequest, RegisterAttorneyRequest, TokenResponse
from app.services.users import authenticate_user, create_pending_attorney, get_user_by_email


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = authenticate_user(db, str(payload.email), payload.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(user.email, user.role.value))


@router.post("/register", response_model=AuthUser, status_code=status.HTTP_201_CREATED)
def register_attorney(payload: RegisterAttorneyRequest, db: Session = Depends(get_db)) -> AuthUser:
    full_name = payload.full_name.strip()
    if not full_name:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Full name is required.")
    existing_user = get_user_by_email(db, str(payload.email))
    if existing_user is not None and existing_user.role == UserRole.PENDING_ATTORNEY and not existing_user.is_active:
        return AuthUser(email=existing_user.email, role=existing_user.role, full_name=existing_user.full_name)
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An account with this email already exists.")
    user = create_pending_attorney(db, full_name, str(payload.email), payload.password)
    return AuthUser(email=user.email, role=user.role, full_name=user.full_name)


@router.get("/me", response_model=AuthUser)
def me(user: User = Depends(require_internal_user)) -> AuthUser:
    return AuthUser(email=user.email, role=user.role, full_name=user.full_name)


@router.get("/attorneys", response_model=AttorneyListResponse)
def list_attorneys(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_user),
) -> AttorneyListResponse:
    users = db.scalars(select(User).where(User.role.in_([UserRole.PENDING_ATTORNEY, UserRole.ATTORNEY])).order_by(User.created_at.desc())).all()
    return AttorneyListResponse(attorneys=[AttorneyRead.model_validate(user, from_attributes=True) for user in users])


@router.patch("/attorneys/{attorney_id}/approve", response_model=AuthUser)
def approve_attorney(
    attorney_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_user),
) -> AuthUser:
    user = db.get(User, attorney_id)
    if user is None or user.role not in {UserRole.PENDING_ATTORNEY, UserRole.ATTORNEY}:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attorney not found")
    user.role = UserRole.ATTORNEY
    user.is_active = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return AuthUser(email=user.email, role=user.role, full_name=user.full_name)
