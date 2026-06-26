# Lead Intake CRM

Lead Intake CRM is a full-stack assignment implementation for public lead submission and internal attorney follow-up.

## Requirement Breakdown

- Public prospects can submit first name, last name, email, and resume/CV.
- A submitted lead is persisted with initial state `PENDING`.
- The app assigns each lead to an active attorney using capacity-based assignment.
- The app sends a confirmation email to the prospect and a case notification email to the assigned attorney.
- Internal users authenticate before viewing lead data.
- Attorneys self-register, wait for admin approval, then can list assigned leads, inspect a lead, and manually mark it `REACHED_OUT`.
- Admins are bootstrapped from environment variables and can approve pending attorney accounts.
- The repo includes a FastAPI backend, Next.js frontend, durable local storage, email integration, a system design document, agent usage notes, and attribution notes.

## Tech Stack

- Backend: FastAPI, SQLAlchemy, SQLite by default, JWT bearer auth.
- Frontend: Next.js App Router, React, TypeScript.
- Email: Mailtrap API/Sandbox when configured, SMTP second, local file outbox fallback.
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
- Attorney registration: `http://localhost:3000/register`
- Internal UI: `http://localhost:3000/leads`
- Attorney management: `http://localhost:3000/admin/attorneys`
- API docs: `http://localhost:8000/docs`

Default bootstrap admin login:

- Email: `admin@example.com`
- Password: `change-me-admin`

Those values come from `BOOTSTRAP_ADMIN_EMAIL` and `BOOTSTRAP_ADMIN_PASSWORD` and seed the initial admin user into the local database on startup. After that, internal authentication is database-backed with salted password hashes, active-account checks, roles, and JWT session verification.

For a real deployment, replace these defaults before first startup. The bootstrap account is the controlled path for creating the first approver; public attorney registration does not create an active internal user by itself.

Attorney onboarding flow:

1. A new attorney opens `/register` and submits name, email, and password.
2. The account is created as pending and inactive.
3. The bootstrap admin logs in and opens `/admin/attorneys`.
4. The admin approves the pending attorney.
5. The approved attorney can log in and receive assigned leads.

Local emails are written to `backend/data/outbox` unless Mailtrap API or SMTP variables are configured.

For the recommended Mailtrap Sandbox demo path, set these in `backend/.env`:

```bash
MAILTRAP_API_TOKEN=your-mailtrap-token
MAILTRAP_FROM_EMAIL=hello@demomailtrap.co
MAILTRAP_FROM_NAME=Alma
MAILTRAP_USE_SANDBOX=true
MAILTRAP_INBOX_ID=your-mailtrap-sandbox-inbox-id
MAILTRAP_SEND_DELAY_SECONDS=6.0
```

Email send order is:

1. Mailtrap API when `MAILTRAP_API_TOKEN`, `MAILTRAP_FROM_EMAIL`, and `MAILTRAP_FROM_NAME` are configured.
2. SMTP when SMTP variables are configured.
3. Local outbox files under `backend/data/outbox`.

When `MAILTRAP_USE_SANDBOX=true`, the backend sends to `https://sandbox.api.mailtrap.io/api/send/{inbox_id}` using `MAILTRAP_INBOX_ID`. Those messages appear in Mailtrap Email Testing / Sandbox, not Gmail or another real recipient mailbox. Sandbox is the recommended demo path because it captures both the customer confirmation and assigned-attorney notification regardless of the recipient address.

Mailtrap Sandbox free plans can rate-limit back-to-back API sends. `MAILTRAP_SEND_DELAY_SECONDS` defaults to `6.0`; the backend sends the customer confirmation first, waits for that short delay, then sends the assigned-attorney notification. Both messages should appear in the same Mailtrap Email Testing / Sandbox inbox, so wait a few seconds and refresh before checking for the second message.

Real Mailtrap Email Sending with `demomailtrap.co` can only send to the Mailtrap account owner in this setup. Use sandbox mode or local outbox when you need to show both customer and attorney messages for arbitrary demo recipients.

The Mailtrap API token is different from Mailtrap SMTP credentials. Mailtrap SMTP sandbox remains an alternate demo path if SMTP settings are configured; otherwise, leave provider settings unset and use the deterministic local outbox. If the Mailtrap API returns a permission error such as `403`, the app preserves the generated emails in `backend/data/outbox` and the lead flow should not crash.

Never commit `backend/.env` or pasted provider secrets. Rotate any Mailtrap token or SMTP password that was pasted into a demo, terminal, or chat after the demo is complete.

Lead assignment is not tied to a hardcoded attorney email. Each new lead is routed to the active approved attorney with the fewest pending assigned leads, with deterministic tie-breakers.

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
2. Register an attorney at `/register`.
3. Confirm the pending attorney cannot log in before approval.
4. Log in as the bootstrap admin and approve the attorney at `/admin/attorneys`.
5. Open the public form and submit a lead with a PDF, DOC, or DOCX resume.
6. Confirm a success message and customer/attorney emails through Mailtrap or local files in `backend/data/outbox`.
7. Confirm the attorney notification is addressed to the assigned approved attorney, not a hardcoded email.
8. Log in as the approved attorney at `/leads`.
9. Confirm the assigned lead appears with `PENDING` state.
10. Open the lead detail page.
11. Click `Mark reached out`.
12. Confirm the state changes to `REACHED OUT`.

## Submission Documents

- [System design](docs/SYSTEM_DESIGN.md)
- [Coding agent usage](docs/AGENT_USAGE.md)
- [Representative prompt logs](docs/PROMPT_LOGS.md)
- [Attribution notes](NOTES.md)
- [Submission checklist](docs/SUBMISSION_CHECKLIST.md)
