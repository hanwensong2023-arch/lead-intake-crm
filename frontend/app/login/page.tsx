"use client";

import { FormEvent, useState } from "react";
import { LogIn } from "lucide-react";
import { useRouter } from "next/navigation";
import { login, setToken } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    const formData = new FormData(event.currentTarget);
    try {
      const token = await login(String(formData.get("email")), String(formData.get("password")));
      setToken(token);
      router.push("/leads");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to log in.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <section className="panel" style={{ maxWidth: 440, margin: "0 auto" }}>
        <form className="form" onSubmit={onSubmit}>
          <h1 style={{ margin: 0 }}>Internal login</h1>
          <div className="field">
            <label className="label" htmlFor="email">
              Email
            </label>
            <input className="input" id="email" name="email" type="email" autoComplete="email" required />
          </div>
          <div className="field">
            <label className="label" htmlFor="password">
              Password
            </label>
            <input className="input" id="password" name="password" type="password" autoComplete="current-password" required />
          </div>
          {error ? (
            <div className="message error" role="alert">
              {error}
            </div>
          ) : null}
          <button className="button" type="submit" disabled={loading}>
            <LogIn size={18} />
            {loading ? "Logging in" : "Log in"}
          </button>
        </form>
      </section>
    </main>
  );
}
