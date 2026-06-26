"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight, LogOut, RefreshCw, Settings } from "lucide-react";
import { ApiError, AuthUser, clearToken, fetchLeads, getToken, Lead, verifySession } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function LeadsPage() {
  const router = useRouter();
  const [leads, setLeads] = useState<Lead[]>([]);
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadLeads = useCallback(async () => {
    if (!getToken()) {
      router.push("/login");
      return;
    }
    setLoading(true);
    setError("");
    try {
      setUser(await verifySession());
      setLeads(await fetchLeads());
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to load leads.");
      if (caught instanceof ApiError && caught.status === 401) {
        clearToken();
        router.push("/login");
      }
    } finally {
      setLoading(false);
    }
  }, [router]);

  useEffect(() => {
    loadLeads();
  }, [loadLeads]);

  function logout() {
    clearToken();
    router.push("/login");
  }

  return (
    <main className="container">
      <div className="toolbar">
        <h1>Leads</h1>
        <div className="nav">
          {user ? <span className="muted">Signed in as {user.email}</span> : null}
          {user?.role === "ADMIN" ? (
            <Link className="text-button" href="/admin/attorneys">
              <Settings size={15} /> Attorneys
            </Link>
          ) : null}
          <button className="text-button" type="button" onClick={loadLeads}>
            <RefreshCw size={15} /> Refresh
          </button>
          <button className="text-button" type="button" onClick={logout}>
            <LogOut size={15} /> Log out
          </button>
        </div>
      </div>

      {loading ? <div className="panel">Loading leads...</div> : null}
      {error && !loading ? (
        <div className="message error" role="alert">
          {error}
        </div>
      ) : null}
      {!loading && !error && leads.length === 0 ? <div className="panel">No leads have been submitted yet.</div> : null}

      <section className="grid" aria-label="Lead list">
        {leads.map((lead) => (
          <Link className="card" key={lead.id} href={`/leads/${lead.id}`}>
            <div>
              <div className="name">
                {lead.first_name} {lead.last_name}
              </div>
              <div className="muted">
                {lead.email} - {new Date(lead.created_at).toLocaleString()}
              </div>
              {lead.assigned_attorney_email ? <div className="muted">Assigned to {lead.assigned_attorney_email}</div> : null}
            </div>
            <StatusBadge state={lead.state} />
            <ArrowRight aria-hidden size={18} />
          </Link>
        ))}
      </section>
    </main>
  );
}

function StatusBadge({ state }: { state: Lead["state"] }) {
  return <span className={`badge ${state === "PENDING" ? "pending" : "reached"}`}>{state.replace("_", " ")}</span>;
}
