from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.lead import LeadState


class LeadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    first_name: str
    last_name: str
    email: EmailStr
    resume_filename: str
    resume_content_type: str
    state: LeadState
    created_at: datetime
    updated_at: datetime
    reached_out_at: datetime | None
    reached_out_by: str | None


class LeadListResponse(BaseModel):
    leads: list[LeadRead]


class LeadCreateResponse(BaseModel):
    id: str
    state: LeadState
    message: str
