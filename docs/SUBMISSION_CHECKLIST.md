# Submission Checklist

## GitHub

- [ ] Public GitHub repository created.
- [ ] Code committed once final verification is complete.
- [ ] No `.env`, local database files, uploads, or node modules committed.
- [ ] README includes local setup and run instructions.
- [ ] System design document included.
- [ ] Agent usage document included.
- [ ] Representative prompt logs included.
- [ ] Attribution notes included.
- [ ] Separate backend/frontend/docs/verification/coordinator agent task files included.
- [ ] Docs cover bootstrap admin, attorney registration, pending approval, admin approval, capacity assignment, no hardcoded attorney email, customer confirmation email, assigned-attorney notification email, and Option D future improvement.
- [ ] Docs cover Mailtrap Sandbox API, `MAILTRAP_USE_SANDBOX`, `MAILTRAP_INBOX_ID`, `MAILTRAP_SEND_DELAY_SECONDS`, SMTP fallback, local outbox fallback, Mailtrap permission-error preservation, and API-token-vs-SMTP-credential distinction.
- [ ] Backend tests pass.
- [ ] Frontend production build passes.
- [ ] Browser smoke test covers registration, pending-login rejection, admin approval, submit, login, list/detail, and status update.
- [ ] Browser smoke test confirms the customer email appears first and assigned-attorney email appears after the short delay through Mailtrap Email Testing / Sandbox, Mailtrap SMTP sandbox, or local outbox.
- [ ] `backend/.env` and any pasted provider secrets are not committed; pasted Mailtrap tokens or SMTP passwords are rotated after the demo.
- [ ] Coordinator reused existing agent sessions/task files or received user approval before creating any new agent.
- [ ] Final GitHub URL pasted into the assignment submission.

## Screen Recording

Record a short E2E workflow:

1. Start the backend and frontend.
2. Register a new attorney and show the pending-approval message.
3. Attempt login as the pending attorney and show that approval is required.
4. Log in as the bootstrap admin and approve the attorney.
5. Submit a public lead with resume upload.
6. Show the customer confirmation in Mailtrap Email Testing / Sandbox or `backend/data/outbox`.
7. Show the assigned-attorney notification after the short delay.
8. If Mailtrap API permissions fail, show that outbox files still preserve the emails and the lead flow did not crash.
9. Show assignment to the approved attorney.
10. Log in as the approved attorney.
11. Open the assigned lead.
12. Mark the lead as reached out.
13. Show the updated status.

Suggested length: 3 to 5 minutes.

Final Loom or screen recording URL:

```text
TBD
```

Final GitHub repository URL:

```text
TBD
```
