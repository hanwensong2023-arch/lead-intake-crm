# Assignment Requirements

## Functional Requirements

Develop an application to support creating, getting and updating leads.

A lead is a form publicly available for prospects to fill in. The required fields include:

- First name
- Last name
- Email
- Resume / CV

Once the lead is submitted by a prospect, the application will send emails to both:

- The prospect
- An attorney inside the company

In addition, the application powers an internal UI guarded by auth to render a list of leads with all the information filled in by the prospect.

Each lead also has a state:

- It starts with a `PENDING` state.
- It transitions to `REACHED_OUT` when marked manually by an attorney after he or she reaches out to the prospect.

## Tech Requirements

- Create a system design to fulfill the above requirements.
- Develop the web app and APIs end to end using coding agents of your choice.
- APIs must be implemented using FastAPI.
- The web app must use Next.js.
- Add storage to persist data.
- Integrate with an email service.
- Structure the code similarly to a production-level repository.

## Submission Guidance

- Submit code to a publicly available GitHub repo.
- Submit a document on how to run the application locally in the same repo.
- Submit a design document explaining why and how design choices were made in the same repo.
- Submit a document describing coding-agent usage. Heavy use is encouraged.
- Include a short writeup, half page max:
  - Which tools were used.
  - What was delegated vs. written directly and why.
  - One place the agent produced wrong or subtly bad code.
  - How it was caught and fixed.
- Include representative prompt logs or session transcript excerpts.
- Include attribution in commits or a `NOTES` file marking agent-generated vs. hand-written code.
- Upload the GitHub link in the assignment document within 6 hours since starting the exercise.
- Upload a short screen recording, such as Loom, showing the end-to-end workflow.

## User Operating Requirements For This Build

1. Break down the requirement.
2. Provide as many agents as needed to work in parallel.
3. Provide a tech design plan.
4. Provide an agent assignment structure.
5. Upload to GitHub after finishing, only once.
6. Save the original requirement as markdown.
7. Save each agent's task as a separate markdown file.
8. The verification agent must use this original assignment requirement as the passing criteria.

## Alma Product Decisions Added During Build

These decisions refine the internal attorney workflow while preserving the original assignment requirements:

- Bootstrap the first admin from environment variables rather than hardcoding a credential in application code.
- Add attorney self-registration.
- Keep newly registered attorneys pending and inactive until admin approval.
- Add admin attorney-management UI and API behavior for approving attorneys.
- Do not email a hardcoded internal attorney.
- Assign each submitted lead to an active approved attorney using capacity-based routing.
- Send the prospect a confirmation email without internal attorney assignment details.
- Send the assigned attorney a case notification email containing:
  - Customer name
  - Customer email
  - Lead ID
  - Resume/CV filename or reference
  - Assigned timestamp
- Support Mailtrap API as the first email provider path, SMTP as the second path, and local outbox as the fallback.
- Support Mailtrap Sandbox mode with `MAILTRAP_USE_SANDBOX=true` and `MAILTRAP_INBOX_ID`, sending to `https://sandbox.api.mailtrap.io/api/send/{inbox_id}`.
- Support `MAILTRAP_SEND_DELAY_SECONDS`, defaulting to `6.0`, so Mailtrap Sandbox demos do not hit free-plan rate limits on back-to-back customer and attorney emails.
- Document that sandbox emails appear in Mailtrap Email Testing / Sandbox, not Gmail, and are recommended for demo because they capture both customer and attorney messages regardless of recipient.
- Document that the customer confirmation email sends first and the assigned-attorney notification sends after a short delay.
- Document that real Mailtrap Email Sending with `demomailtrap.co` can only send to the account owner in this setup.
- Preserve local outbox email files if Mailtrap API returns a permission error so the lead flow remains verifiable.
- Track Option D, AI-assisted assignment, as a future improvement rather than implementing it in this assignment build.

## Documentation Deliverables In This Repo

- Local run instructions: `README.md`.
- System design and design rationale: `docs/SYSTEM_DESIGN.md`.
- Coding-agent usage writeup: `docs/AGENT_USAGE.md`.
- Prompt/session excerpts: `docs/PROMPT_LOGS.md`.
- Attribution notes: `NOTES.md`.
- Separate agent task files: `docs/agents/01_backend_agent.md`, `docs/agents/02_frontend_agent.md`, `docs/agents/03_docs_agent.md`, `docs/agents/04_verification_agent.md`, and `docs/agents/05_coordinator_agent.md`.
- Final submission and screen-recording checklist: `docs/SUBMISSION_CHECKLIST.md`.

## Coordinator Agent Rule

- Reuse existing agent sessions and markdown task files when new work fits an existing lane.
- Update existing agent responsibilities instead of creating duplicate agents for the same lane.
- Ask for user approval before creating a new agent or new agent session.
