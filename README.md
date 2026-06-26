# Lead Intake CRM

Lead Intake CRM is a full-stack assignment implementation for public lead submission and internal attorney follow-up.

## Requirement Breakdown

- Public prospects can submit first name, last name, email, and resume/CV.
- A submitted lead is persisted with initial state `PENDING`.
- The app sends notification emails to the prospect and the internal attorney.
- Internal users authenticate before viewing lead data.
- Attorneys can list leads, inspect a lead, and manually mark it `REACHED_OUT`.
- The repo includes a FastAPI backend, Next.js frontend, durable local storage, email integration, a system design document, agent usage notes, and attribution notes.

## Tech Stack

- Backend: FastAPI, SQLAlchemy, SQLite by default, JWT bearer auth.
- Frontend: Next.js App Router, React, TypeScript.
- Email: SMTP when configured; local file outbox in development.
- Uploads: local filesystem storage in development with MIME and size validation.

## Run Locally

Prerequisites:

- Python 3.11+
- Node.js 20.9+

Start the backend:

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Start the frontend in another terminal:

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Open:

- Public form: `http://localhost:3000`
- Internal UI: `http://localhost:3000/leads`
- API docs: `http://localhost:8000/docs`

Default internal login:

- Email: `attorney@example.com`
- Password: `change-me`

Those values seed the initial attorney user into the local database on startup. After that, attorney authentication is database-backed with salted password hashes and JWT session verification.

Local emails are written to `backend/data/outbox` unless SMTP variables are configured.

## Useful Commands

```bash
cd backend && pytest
cd frontend && npm run build
```

## Environment Variables

Backend variables are documented in `backend/.env.example`.

Frontend variables are documented in `frontend/.env.example`.

For local browser testing, the backend allows both `http://localhost:3000` and `http://127.0.0.1:3000` by default.

## Demo Flow

1. Start backend and frontend.
2. Open the public form and submit a lead with a PDF, DOC, or DOCX resume.
3. Confirm a success message.
4. Open `/leads`; log in if redirected.
5. Confirm the new lead appears with `PENDING` state.
6. Open the lead detail page.
7. Click `Mark reached out`.
8. Confirm the state changes to `REACHED OUT`.

## Submission Documents

- [System design](docs/SYSTEM_DESIGN.md)
- [Coding agent usage](docs/AGENT_USAGE.md)
- [Representative prompt logs](docs/PROMPT_LOGS.md)
- [Attribution notes](NOTES.md)
- [Submission checklist](docs/SUBMISSION_CHECKLIST.md)
