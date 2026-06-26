"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { ClipboardCheck, UserPlus } from "lucide-react";
import { registerAttorney } from "@/lib/api";

export default function RegisterPage() {
  const [error, setError] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    setLoading(true);
    setError("");
    setSubmitted(false);
    const formData = new FormData(form);
    try {
      await registerAttorney(
        String(formData.get("fullName")),
        String(formData.get("email")),
        String(formData.get("password"))
      );
      setSubmitted(true);
      form.reset();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to submit registration.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <section className="panel" style={{ maxWidth: 520, margin: "0 auto" }}>
        <form className="form" onSubmit={onSubmit}>
          <h1 style={{ margin: 0 }}>Attorney registration</h1>
          <div className="field">
            <label className="label" htmlFor="fullName">
              Full name
            </label>
            <input className="input" id="fullName" name="fullName" type="text" autoComplete="name" required />
          </div>
          <div className="field">
            <label className="label" htmlFor="email">
              Work email
            </label>
            <input className="input" id="email" name="email" type="email" autoComplete="email" required />
          </div>
          <div className="field">
            <label className="label" htmlFor="password">
              Password
            </label>
            <input className="input" id="password" name="password" type="password" autoComplete="new-password" minLength={8} required />
          </div>
          {submitted ? (
            <div className="message ok" role="status">
              <ClipboardCheck size={17} />
              Registration submitted. An admin must approve the account before login.
            </div>
          ) : null}
          {error ? (
            <div className="message error" role="alert">
              {error}
            </div>
          ) : null}
          <button className="button" type="submit" disabled={loading}>
            <UserPlus size={18} />
            {loading ? "Submitting" : "Request access"}
          </button>
          <Link className="text-button" href="/login">
            Already approved? Log in
          </Link>
        </form>
      </section>
    </main>
  );
}
