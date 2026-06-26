# Coordinator Agent Task

## Mission

Coordinate the build, integrate agent outputs, run final verification, and upload to GitHub once.

## Source Of Truth

Use `docs/ASSIGNMENT_REQUIREMENTS.md` as the source of truth.

## Responsibilities

- Maintain the global plan.
- Assign work to backend, frontend, docs, and verification agents.
- Reuse the existing agent sessions and their markdown responsibility files.
- Update an existing agent's task or responsibility when the work fits that agent's markdown lane.
- Ask for user approval before creating any new agent or new agent session.
- Avoid overlapping edit ownership between agents.
- Integrate completed work.
- Resolve conflicts.
- Ensure verification runs against the original assignment.
- Ensure Alma product decisions are integrated:
  - Bootstrap admin from environment variables.
  - Attorney self-registration with pending approval.
  - Admin attorney approval.
  - Capacity-based assignment to active approved attorneys.
  - No hardcoded attorney email.
  - Customer email plus assigned-attorney case notification.
  - Option D AI-assisted assignment documented as future improvement.
- Commit final work.
- Upload to a public GitHub repo only once after verification is acceptable.
- Provide the final repo link and screen recording checklist.

## Automatic Verification Policy

Preferred workflow:

1. Implementation agent finishes and reports changed files plus test results.
2. Coordinator immediately sends that summary to the verification agent.
3. Verification agent checks the work against `docs/ASSIGNMENT_REQUIREMENTS.md`.
4. Coordinator fixes or delegates any blockers.
5. Final upload happens only after verification is `PASS` or an explicitly accepted `PASS WITH RISKS`.

## Completion Output

Report:

- Final requirement coverage.
- Agents used.
- Verification result.
- GitHub repo URL.
- Any remaining manual step, such as recording or pasting the Loom URL.
