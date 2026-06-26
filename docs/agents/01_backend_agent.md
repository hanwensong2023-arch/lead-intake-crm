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
- Email notification to assigned attorney after submission.
- No hardcoded attorney email for lead notifications.
- Capacity-based assignment to an active approved attorney during lead creation.
- Assignment fields persisted on each lead:
  - Assigned attorney ID
  - Assigned attorney email
  - Assigned timestamp
- Bootstrap admin from environment variables.
- Attorney self-registration creates a pending inactive account.
- Admin-only attorney listing and approval endpoints.
- Pending attorneys cannot log in or receive assignments.
- Mailtrap API path using `MAILTRAP_API_TOKEN`, `MAILTRAP_FROM_EMAIL`, and `MAILTRAP_FROM_NAME`.
- Mailtrap Sandbox mode using `MAILTRAP_USE_SANDBOX=true` and `MAILTRAP_INBOX_ID`, sending to `https://sandbox.api.mailtrap.io/api/send/{inbox_id}`.
- SMTP provider path when SMTP variables are configured.
- Local development email mode, such as file outbox or console sink.
- Email send order: Mailtrap API first, SMTP second, local outbox fallback.
- Mailtrap API permission failures preserve emails in local outbox and do not crash the lead flow.
- Production-shaped email adapter boundary for Mailtrap API, SMTP, or another provider integration.
- Resume upload validation:
  - File required.
  - Allowed types documented and enforced.
  - Size cap enforced.
  - Original filename not trusted as storage path.
- Environment-based settings.
- Tests for happy path, auth failure, upload validation, state transition, attorney registration approval, and least-loaded attorney assignment.

## Preferred Design

- FastAPI for API.
- SQLAlchemy for ORM.
- SQLite locally with `DATABASE_URL` support for Postgres later.
- JWT or session-based internal auth.
- Service layer for email and storage.
- Keep assignment logic in a service so routing can evolve to AI-assisted assignment later without rewriting lead creation.

## Completion Output

When done, report:

- Files changed.
- API endpoints implemented.
- How persistence works.
- How email works locally and in production config.
- How provider failures fall back or preserve local evidence.
- Tests run and results.
- Known risks or limitations.
