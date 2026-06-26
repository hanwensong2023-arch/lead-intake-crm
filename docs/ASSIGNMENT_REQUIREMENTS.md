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
