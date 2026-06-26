# Documentation Agent Task

## Mission

Create and verify all documentation required for assignment submission.

## Source Of Truth

Read `docs/ASSIGNMENT_REQUIREMENTS.md` first. Documentation is complete only if it covers the original assignment requirements.

## Ownership

Own documentation files under:

- `README.md`
- `docs`
- `NOTES.md`

Coordinate before editing application code.

## Required Documents

- Local run instructions in the repo.
- System design document explaining why and how design choices were made.
- Design coverage for bootstrap admin, production auth, attorney self-registration, pending approval, admin approval, capacity-based assignment, and email recipient behavior.
- Email documentation for Mailtrap Sandbox API, `MAILTRAP_USE_SANDBOX`, `MAILTRAP_INBOX_ID`, `MAILTRAP_SEND_DELAY_SECONDS`, SMTP fallback, local outbox fallback, Mailtrap permission-error preservation, and provider secret hygiene.
- Future improvement note for Option D, AI-assisted assignment.
- Coding-agent usage document.
- Representative prompt logs or transcript excerpts.
- Attribution notes marking agent-generated vs. hand-written or human-reviewed work.
- Explicit note that no hardcoded attorney email should remain in the documented workflow.
- Screen recording checklist or instructions.
- GitHub submission checklist.

## Required Agent Usage Writeup

Keep the main writeup half a page max and include:

- Tools used.
- What was delegated vs. written directly and why.
- One place the agent produced wrong or subtly bad code.
- How it was caught and fixed.

## Completion Output

When done, report:

- Files changed.
- Which assignment documentation requirements are satisfied.
- Any missing user-provided item, such as final Loom URL or GitHub URL.
- Confirmation that no application code or secret-bearing `.env` files were edited.
