# Representative Prompt Logs

These excerpts document how coding agents were used during the assignment. They are representative rather than full transcripts.

## Coordinator Prompt

```text
You got the following requirements:
Assignment Functional Requirements...
You need to:
1. break down the requirement,
2. provide as many agents as you need to work in parallel,
3. provide me a tech design plan,
4. provide me an agents assignments structure,
5. upload to git hub after you finish it, you only need to upload once.
```

## Alma Decision Update Prompt

```text
Update the implementation and docs for the latest Alma decisions:
bootstrap the first admin from env, allow attorney self-registration only into
a pending approval state, add admin attorney approval, assign new leads by
capacity across active approved attorneys, remove the hardcoded attorney email,
send a customer confirmation email, send the assigned attorney a case
notification email, and document Option D AI-assisted assignment as a future
improvement rather than building it now.
```

## Backend Agent Prompt

```text
You are Agent A: backend/API reviewer for a greenfield lead intake CRM assignment.
Produce a concise backend design checklist and API contract for FastAPI covering:
public lead submit with resume upload, internal auth-guarded lead list/detail,
status transition PENDING -> REACHED_OUT, persistence, email service abstraction,
security validation, and tests.
```

## Alma Auth And Assignment Follow-Up

```text
This is Alma, an immigration AI service company. When a customer sends their name,
email, and CV, the info should be sent to the customer and an attorney should be
assigned by this info. Use Option B capacity-based assignment now, and write
Option D AI-assisted assignment into the future improvement plan. Add attorney
registration, pending approval, bootstrap admin, and email the assigned attorney
instead of a hardcoded internal attorney.
```

## Frontend Agent Prompt

```text
You are Agent B: frontend/internal UI reviewer for a greenfield lead intake CRM assignment.
Produce a concise Next.js app structure and UX checklist covering:
public lead form with resume upload, internal login, auth-guarded leads list,
lead detail, mark reached out action, env config, accessible states/errors/loading,
and E2E demo flow.
```

## Documentation Agent Prompt

```text
You are Agent C: documentation/submission reviewer for a greenfield assignment.
Draft concise sections for README, SYSTEM_DESIGN, AGENT_USAGE, and NOTES attribution.
Requirements: how to run locally, design choices, coding-agent usage writeup <= half page,
representative prompt excerpts, attribution, Loom/screen-recording checklist,
and GitHub submission checklist.
```

## Verification Agent Prompt

```text
Verify the completed application and documentation against docs/ASSIGNMENT_REQUIREMENTS.md.
Use the original assignment as the passing criteria, not the implementation plan.
Report PASS, PASS WITH RISKS, or FAIL, with missing requirements and commands run.
```

## Docs Agent Delegation Prompt

```text
Update markdown/docs only so the repo clearly covers the original assignment,
local run instructions, system design, agent usage writeup, prompt/session
excerpts, attribution notes, and the latest Alma decisions. Ensure separate
agent-task markdown files exist for coordinator, backend, frontend, docs, and
verification. Do not edit application code. Report changed files and
assumptions.
```

## Email Implementation Docs Prompt

```text
Docs Agent task per docs/agents/03_docs_agent.md: update markdown/docs for the
latest email implementation and decisions. No code edits. Cover: backend now
supports Mailtrap Sending API via MAILTRAP_API_TOKEN / MAILTRAP_FROM_EMAIL /
MAILTRAP_FROM_NAME; send order is Mailtrap API first, SMTP second, local outbox
fallback; if Mailtrap API returns 403/permission error, app preserves emails in
backend/data/outbox and lead flow should not crash; Mailtrap API token is
different from Mailtrap SMTP credentials; easiest demo path may be Mailtrap SMTP
sandbox or local outbox; do not commit backend/.env secrets; rotate pasted
tokens after demo. Also ensure docs reflect the coordinator rule: reuse existing
agent sessions/MD files, update existing agent responsibilities when
appropriate, ask user approval before creating new agents.
```

## Final Mailtrap Sandbox Docs Prompt

```text
Docs Agent update per docs/agents/03_docs_agent.md: update docs to reflect final
Mailtrap Sandbox behavior. No code edits. Backend now supports
MAILTRAP_USE_SANDBOX=true and MAILTRAP_INBOX_ID; when sandbox is enabled, emails
send to https://sandbox.api.mailtrap.io/api/send/{inbox_id} and appear in
Mailtrap Email Testing/Sandbox inbox, not Gmail. Real Email Sending with
demomailtrap.co can only send to account owner; sandbox is recommended for demo
because it captures both customer and attorney messages regardless of recipient.
Keep notes about MAILTRAP_API_TOKEN, MAILTRAP_FROM_EMAIL, MAILTRAP_FROM_NAME,
SMTP fallback, local outbox fallback, and not committing backend/.env secrets.
```

## Final Email Delay Docs Prompt

```text
Docs Agent task per docs/agents/03_docs_agent.md: final docs cleanup for email.
No code edits. Document final Mailtrap Sandbox demo path: MAILTRAP_API_TOKEN,
MAILTRAP_USE_SANDBOX=true, MAILTRAP_INBOX_ID, MAILTRAP_FROM_EMAIL,
MAILTRAP_FROM_NAME, MAILTRAP_SEND_DELAY_SECONDS default 6.0 because Mailtrap
Sandbox free plan rate-limits back-to-back emails. Explain that after lead
submission the customer email sends first and attorney notification sends after
a short delay, both visible in Mailtrap Email Testing/Sandbox inbox. Keep notes
on SMTP fallback and local outbox fallback. Warn not to commit backend/.env
secrets and rotate pasted tokens after demo.
```
