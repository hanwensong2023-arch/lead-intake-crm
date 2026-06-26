"use client";

import { FormEvent, useState } from "react";
import { Send, Upload } from "lucide-react";
import { submitLead } from "@/lib/api";

export default function PublicLeadPage() {
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [message, setMessage] = useState("");

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    setStatus("loading");
    setMessage("");

    try {
      const formData = new FormData(form);
      const payload = await submitLead(formData);
      form.reset();
      setStatus("success");
      setMessage(payload.message);
    } catch (error) {
      setStatus("error");
      setMessage(error instanceof Error ? error.message : "Unable to submit lead.");
    }
  }

  return (
    <main className="container split">
      <section>
        <h1 className="headline">Start a confidential intake request.</h1>
        <p className="lede">
          Prospects can send their contact details and resume directly to the internal attorney team.
          Submitted leads are stored for review and begin in a pending state.
        </p>
      </section>

      <section className="panel" aria-label="Lead intake form">
        <form className="form" onSubmit={onSubmit}>
          <div className="field">
            <label className="label" htmlFor="first_name">
              First name
            </label>
            <input className="input" id="first_name" name="first_name" autoComplete="given-name" required />
          </div>
          <div className="field">
            <label className="label" htmlFor="last_name">
              Last name
            </label>
            <input className="input" id="last_name" name="last_name" autoComplete="family-name" required />
          </div>
          <div className="field">
            <label className="label" htmlFor="email">
              Email
            </label>
            <input className="input" id="email" name="email" type="email" autoComplete="email" required />
          </div>
          <div className="field">
            <label className="label" htmlFor="resume">
              Resume / CV
            </label>
            <input
              className="input"
              id="resume"
              name="resume"
              type="file"
              accept=".pdf,.doc,.docx,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
              required
            />
          </div>
          {message ? (
            <div className={`message ${status === "success" ? "ok" : "error"}`} role="alert">
              {message}
            </div>
          ) : null}
          <button className="button" type="submit" disabled={status === "loading"}>
            {status === "loading" ? <Upload size={18} /> : <Send size={18} />}
            {status === "loading" ? "Submitting" : "Submit lead"}
          </button>
        </form>
      </section>
    </main>
  );
}
