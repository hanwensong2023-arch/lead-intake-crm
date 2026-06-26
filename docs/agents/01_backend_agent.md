# Backend Agent Task

## Mission

Build and verify the FastAPI backend for the Lead Intake CRM assignment.

## Source Of Truth

Read `docs/ASSIGNMENT_REQUIREMENTS.md` first. The backend is complete only if it supports the original assignment requirements.

## Ownership

Own backend files under:

- `backend/app`
- `backend/tests`
- `backend/requirements.txt`
- `backend/.env.example`

Do not edit frontend files unless the coordinator explicitly asks.

## Required Backend Capabilities

- Public unauthenticated lead creation endpoint.
- Required lead fields:
  - First name
  - Last name
  - Email
  - Resume / CV
- Persistent lead storage.
- Lead state starts as `PENDING`.
- Auth-protected internal lead list endpoint.
- Auth-protected internal lead detail endpoint.
- Auth-protected lead update endpoint that manually marks a lead `REACHED_OUT`.
- Email notification to prospect after submission.
- Email notification to internal attorney after submission.
- Local development email mode, such as file outbox or console sink.
- Production-shaped email adapter boundary for SMTP or provider integration.
- Resume upload validation:
  - File required.
  - Allowed types documented and enforced.
  - Size cap enforced.
  - Original filename not trusted as storage path.
- Environment-based settings.
- Tests for happy path, auth failure, upload validation, and state transition.

## Preferred Design

- FastAPI for API.
- SQLAlchemy for ORM.
- SQLite locally with `DATABASE_URL` support for Postgres later.
- JWT or session-based internal auth.
- Service layer for email and storage.

## Completion Output

When done, report:

- Files changed.
- API endpoints implemented.
- How persistence works.
- How email works locally and in production config.
- Tests run and results.
- Known risks or limitations.
