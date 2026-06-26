# Coding Agent Usage

Coding agents were used heavily for planning, implementation, review, and documentation. The main Codex agent implemented the repository locally, while parallel subagents reviewed backend API design, frontend workflow expectations, and submission documentation.

Delegated work:

- Backend/API reviewer: API contract, persistence checklist, upload and email risks.
- Frontend reviewer: Next.js route structure, UX states, auth flow, E2E demo path.
- Documentation reviewer: README, design doc, agent usage, attribution, and submission checklist outline.

Main-thread work:

- Final architecture choices.
- FastAPI implementation.
- Next.js implementation.
- Documentation integration.
- Verification and fixes.
- Git/GitHub submission.

One place the agent produced subtly bad code: the backend initially allowed CORS only for `http://localhost:3000`. During browser smoke testing, the Next.js dev server was reached at `http://127.0.0.1:3000`, so login failed with `Failed to fetch`. I caught it in the browser flow and fixed the backend settings to allow both local origins through `FRONTEND_ORIGIN` and `EXTRA_CORS_ORIGINS`.

Representative prompt/session excerpts are in `docs/PROMPT_LOGS.md`.

All generated code and prose was reviewed before inclusion. The submitted files should be treated as AI-assisted and human-reviewed.
