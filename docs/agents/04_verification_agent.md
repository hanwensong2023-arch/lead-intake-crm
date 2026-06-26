# Verification Agent Task

## Mission

Verify the completed application and documentation against the original assignment.

## Passing Criteria Source

Use `docs/ASSIGNMENT_REQUIREMENTS.md` as the source of truth. Do not treat implementation plans, README claims, or agent summaries as passing criteria unless they match the original assignment.

## Ownership

Prefer read-only review. If fixes are needed, report them to the coordinator first unless explicitly assigned a narrow fix.

## Verification Checklist

Functional requirements:

- Public prospect form exists.
- Public form requires first name, last name, email, and resume/CV.
- Lead submission persists data.
- New lead starts as `PENDING`.
- Email is sent or recorded for the prospect.
- Email is sent or recorded for the assigned internal attorney.
- Email send order is Mailtrap API first, SMTP second, local outbox fallback.
- Mailtrap Sandbox mode uses `MAILTRAP_USE_SANDBOX=true`, `MAILTRAP_INBOX_ID`, and the `https://sandbox.api.mailtrap.io/api/send/{inbox_id}` endpoint.
- `MAILTRAP_SEND_DELAY_SECONDS` defaults to `6.0` to avoid Mailtrap Sandbox free-plan rate limits for back-to-back emails.
- Sandbox emails appear in Mailtrap Email Testing / Sandbox, not Gmail.
- Customer confirmation email sends first; assigned-attorney notification sends after the short delay.
- Sandbox demo captures both customer and attorney messages regardless of recipient; real Email Sending with `demomailtrap.co` can only send to the account owner in this setup.
- Mailtrap API permission failures preserve email files in `backend/data/outbox` and do not crash lead submission.
- Mailtrap API token is documented separately from Mailtrap SMTP credentials.
- Attorney email includes customer name, customer email, lead ID, resume/CV reference, and assigned timestamp.
- Prospect email confirms receipt and does not expose internal assignment details.
- Internal UI is guarded by auth.
- New attorneys register into a pending/inactive state.
- Pending attorneys cannot log in.
- Admin can approve pending attorneys.
- Approved active attorneys can log in.
- New leads are assigned to active attorneys by capacity, not by hardcoded email.
- Lead creation fails or otherwise avoids false success when no active approved attorney can receive the case.
- Internal UI renders a list of leads.
- Internal UI shows all prospect-submitted information.
- Attorney can manually mark a lead `REACHED_OUT`.
- Status transition is reflected after update.

Tech requirements:

- API uses FastAPI.
- Web app uses Next.js.
- Persistent storage exists.
- Email service integration exists.
- Email secret hygiene is documented, including not committing `backend/.env` and rotating pasted provider tokens after demos.
- Repo is structured like a production-level project.
- Local run instructions exist.
- System design document exists.
- Coding-agent usage document exists.
- Prompt/session excerpts exist.
- Attribution exists in commits or `NOTES.md`.
- No secrets or local generated artifacts are committed.

Verification commands to run when possible:

- Backend dependency install.
- Backend tests.
- Frontend dependency install.
- Frontend build or lint.
- Manual E2E smoke test:
  - Submit lead.
  - Confirm customer email first, then attorney email after the short delay, through Mailtrap Email Testing / Sandbox, Mailtrap SMTP sandbox, or local outbox.
  - If testing a Mailtrap permission error, confirm local outbox preservation and no lead-flow crash.
  - Register attorney.
  - Log in as admin and approve attorney.
  - Log in as approved attorney.
  - See lead.
  - Mark reached out.
  - Confirm state change.

## Output Format

Report:

- `PASS`, `PASS WITH RISKS`, or `FAIL`.
- Blocking issues, ordered by severity.
- Missing assignment requirements.
- Commands run and results.
- Manual verification notes.
- Final recommendation for whether the coordinator should upload to GitHub.
