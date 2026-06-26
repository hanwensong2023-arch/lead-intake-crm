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

## Backend Agent Prompt

```text
You are Agent A: backend/API reviewer for a greenfield lead intake CRM assignment.
Produce a concise backend design checklist and API contract for FastAPI covering:
public lead submit with resume upload, internal auth-guarded lead list/detail,
status transition PENDING -> REACHED_OUT, persistence, email service abstraction,
security validation, and tests.
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
