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
- Email is sent or recorded for the internal attorney.
- Internal UI is guarded by auth.
- Internal UI renders a list of leads.
- Internal UI shows all prospect-submitted information.
- Attorney can manually mark a lead `REACHED_OUT`.
- Status transition is reflected after update.

Tech requirements:

- API uses FastAPI.
- Web app uses Next.js.
- Persistent storage exists.
- Email service integration exists.
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
  - Confirm email outbox or SMTP behavior.
  - Log in internally.
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
