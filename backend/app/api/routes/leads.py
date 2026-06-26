from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_internal_user
from app.db.session import get_db
from app.models.lead import Lead, LeadState
from app.models.user import User
from app.schemas.lead import LeadCreateResponse, LeadListResponse, LeadRead
from app.services.email import EmailService
from app.services.storage import store_resume


router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("", response_model=LeadCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    first_name: str = Form(..., min_length=1, max_length=80),
    last_name: str = Form(..., min_length=1, max_length=80),
    email: EmailStr = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> LeadCreateResponse:
    first_name = first_name.strip()
    last_name = last_name.strip()
    if not first_name or not last_name:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="First and last name are required.")
    resume_filename, resume_storage_path = await store_resume(resume)
    lead = Lead(
        first_name=first_name,
        last_name=last_name,
        email=str(email).lower(),
        resume_filename=resume_filename,
        resume_content_type=resume.content_type or "application/octet-stream",
        resume_storage_path=resume_storage_path,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    EmailService().send_lead_notifications(lead)
    return LeadCreateResponse(id=lead.id, state=lead.state, message="Lead submitted successfully.")


@router.get("", response_model=LeadListResponse)
def list_leads(
    db: Session = Depends(get_db),
    _: User = Depends(require_internal_user),
) -> LeadListResponse:
    leads = db.scalars(select(Lead).order_by(Lead.created_at.desc())).all()
    return LeadListResponse(leads=list(leads))


@router.get("/{lead_id}", response_model=LeadRead)
def get_lead(
    lead_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_internal_user),
) -> Lead:
    lead = db.get(Lead, lead_id)
    if lead is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return lead


@router.patch("/{lead_id}/reach-out", response_model=LeadRead)
def mark_reached_out(
    lead_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_internal_user),
) -> Lead:
    lead = db.get(Lead, lead_id)
    if lead is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    if lead.state != LeadState.REACHED_OUT:
        lead.state = LeadState.REACHED_OUT
        lead.reached_out_at = datetime.now(UTC)
        lead.reached_out_by = user.email
        db.add(lead)
        db.commit()
        db.refresh(lead)
    return lead


@router.get("/{lead_id}/resume")
def download_resume(
    lead_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_internal_user),
) -> FileResponse:
    lead = db.get(Lead, lead_id)
    if lead is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")

    resume_path = Path(lead.resume_storage_path)
    if not resume_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume file not found")

    return FileResponse(
        path=resume_path,
        media_type=lead.resume_content_type,
        filename=lead.resume_filename,
    )
