# Frontend Agent Task

## Mission

Build and verify the Next.js frontend for the Lead Intake CRM assignment.

## Source Of Truth

Read `docs/ASSIGNMENT_REQUIREMENTS.md` first. The frontend is complete only if it supports the original assignment requirements.

## Ownership

Own frontend files under:

- `frontend/app`
- `frontend/components`
- `frontend/lib`
- `frontend/package.json`
- `frontend/.env.example`

Do not edit backend files unless the coordinator explicitly asks.

## Required Frontend Capabilities

- Public lead form available without auth.
- Form fields:
  - First name
  - Last name
  - Email
  - Resume / CV
- Client-side UX for required fields, loading, success, and error states.
- Internal login page.
- Attorney registration page.
- Pending-registration success message that explains admin approval is required.
- Internal lead list page guarded by backend auth.
- Lead detail page showing all information submitted by the prospect.
- Admin attorney-management page for listing pending/approved attorneys and approving pending attorneys.
- Manual action for attorney to mark the lead `REACHED_OUT`.
- UI refresh after status update so list/detail state does not become stale.
- Environment variable for API base URL.

## UX Requirements

- The first screen should be the usable public intake form, not a marketing landing page.
- Internal UI should be dense, clear, and work-focused.
- Status labels must stay visually contained inside their color block on desktop and mobile.
- Admin-only controls should not appear to ordinary attorneys.
- Inputs must have labels.
- Buttons must show loading/disabled states during requests.
- Errors should be visible and recoverable.
- Mobile layout should not overlap text or controls.

## Completion Output

When done, report:

- Files changed.
- Routes implemented.
- Demo flow.
- Build/lint commands run and results.
- Known risks or limitations.
