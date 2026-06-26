# Coding Agent Usage

Coding agents were used heavily for planning, implementation, review, and documentation. The coordinator agent owned final decisions and integration, while separate specialist agents handled backend, frontend, documentation, and verification tracks.

Tools used included Codex coding sessions, local shell commands, FastAPI and Next.js build/test commands, and repository markdown artifacts for agent prompts and verification criteria.

Coordinator rule: reuse the existing backend, frontend, docs, verification, and coordinator agent sessions and their markdown task files when work fits those lanes. Update the existing responsibilities when appropriate, and ask the user for approval before creating any new agent or new agent session.

Delegated work:

- Backend agent: FastAPI data model, auth lifecycle, lead assignment, email behavior, upload handling, and backend tests.
- Frontend agent: Next.js public intake, attorney registration, admin approval UI, internal lead views, and status UI polish.
- Docs/compliance agent: README, original requirements, system design, agent usage, attribution, and submission checklist.
- Verification agent: Acceptance review against `docs/ASSIGNMENT_REQUIREMENTS.md`, including the original assignment and Alma product decisions.

Coordinator work:

- Final architecture choices.
- Work split and conflict boundaries.
- Integration of specialist outputs.
- Verification and fixes.
- Final Git/GitHub submission.

One place the agent produced subtly bad code: an early email implementation used a hardcoded internal attorney recipient. That passed the literal first version of the assignment but was wrong for Alma's production workflow because leads need an accountable assigned attorney. We caught it during product review, replaced it with capacity-based assignment to active approved attorneys, and updated the attorney notification email to include customer name, customer email, lead ID, resume/CV reference, and assigned timestamp.

The same review also tightened attorney lifecycle behavior: public registration creates pending inactive accounts, the first admin is bootstrapped from environment variables, and admin approval is required before an attorney can log in or receive assignments.

Later email review clarified the provider behavior: the backend tries Mailtrap API first, SMTP second, and local outbox fallback last. The final demo recommendation is Mailtrap Sandbox with `MAILTRAP_USE_SANDBOX=true`, `MAILTRAP_INBOX_ID`, and `MAILTRAP_SEND_DELAY_SECONDS=6.0`, which captures both customer and attorney messages in Mailtrap Email Testing rather than Gmail. The customer email sends first, then the attorney notification sends after the short delay to avoid Mailtrap Sandbox free-plan rate limits. If Mailtrap API permissions fail, the generated emails are preserved in the local outbox so the lead flow remains demoable and debuggable.

Representative prompt/session excerpts are in `docs/PROMPT_LOGS.md`.

All generated code and prose was reviewed before inclusion. The submitted files should be treated as AI-assisted and human-reviewed.
