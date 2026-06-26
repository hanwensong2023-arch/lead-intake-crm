# Agent Assignment Structure

This folder contains one markdown file per agent. Each file is written so it can be pasted directly into a separate Codex session or used as a subagent prompt from the coordinator session.

## Recommended Agent Sessions

- `01_backend_agent.md`: FastAPI, persistence, uploads, email, auth, backend tests.
- `02_frontend_agent.md`: Next.js public form, internal auth UI, lead list/detail/update workflow.
- `03_docs_agent.md`: README, system design, agent usage, attribution, submission checklist.
- `04_verification_agent.md`: Acceptance verification against the original assignment.
- `05_coordinator_agent.md`: Integration, conflict resolution, final GitHub upload, and screen recording prep.

## Coordination Rule

The verification agent should use `docs/ASSIGNMENT_REQUIREMENTS.md` as the source of truth. A feature is passing only if it satisfies the original assignment, not merely an implementation-specific plan.

## Separate Session Workflow

If using visible separate Codex sessions, create one session per agent and paste the corresponding file as the first prompt. Keep the coordinator session open as the owner of final integration.

When an implementation agent finishes, send its final summary, changed file list, and verification commands to the verification agent.
