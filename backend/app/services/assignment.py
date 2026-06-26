from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.lead import Lead, LeadState
from app.models.user import User, UserRole


def assign_lead_to_attorney(db: Session, lead: Lead) -> User:
    open_counts = (
        select(Lead.assigned_attorney_id, func.count(Lead.id).label("open_count"))
        .where(Lead.state == LeadState.PENDING, Lead.assigned_attorney_id.is_not(None))
        .group_by(Lead.assigned_attorney_id)
        .subquery()
    )
    attorney = db.scalar(
        select(User)
        .outerjoin(open_counts, User.id == open_counts.c.assigned_attorney_id)
        .where(User.role == UserRole.ATTORNEY, User.is_active.is_(True))
        .order_by(func.coalesce(open_counts.c.open_count, 0), User.last_assigned_at.is_not(None), User.last_assigned_at, User.email)
        .limit(1)
    )
    if attorney is None:
        raise ValueError("No active attorneys are available for assignment.")

    assigned_at = datetime.now(UTC)
    lead.assigned_attorney_id = attorney.id
    lead.assigned_attorney_email = attorney.email
    lead.assigned_at = assigned_at
    attorney.last_assigned_at = assigned_at
    db.add(lead)
    db.add(attorney)
    return attorney
