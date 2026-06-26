"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { CheckCircle2, ChevronLeft, Download, LogOut } from "lucide-react";
import { ApiError, AuthUser, clearToken, downloadResume, fetchLead, getToken, Lead, markReachedOut, verifySession } from "@/lib/api";
import { useParams, useRouter } from "next/navigation";

export default function LeadDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [lead, setLead] = useState<Lead | null>(null);
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState("");

  const loadLead = useCallback(async () => {
    if (!getToken()) {
      router.push("/login");
      return;
    }
    try {
      setUser(await verifySession());
      setLead(await fetchLead(id));
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to load lead.");
      if (caught instanceof ApiError && caught.status === 401) {
        clearToken();
        router.push("/login");
      }
    } finally {
      setLoading(false);
    }
  }, [id, router]);

  useEffect(() => {
    loadLead();
  }, [loadLead]);

  async function onMarkReachedOut() {
    setSaving(true);
    setError("");
    try {
      setLead(await markReachedOut(id));
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to update lead.");
    } finally {
      setSaving(false);
    }
  }

  async function onDownloadResume() {
    if (!lead) return;
    setDownloading(true);
    setError("");
    try {
      const blob = await downloadResume(id);
      const url = window.URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = lead.resume_filename;
      document.body.append(anchor);
      anchor.click();
      anchor.remove();
      window.URL.revokeObjectURL(url);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to download resume.");
    } finally {
      setDownloading(false);
    }
  }

  function logout() {
    clearToken();
    router.push("/login");
  }

  return (
    <main className="container">
      <div className="toolbar">
        <Link className="text-button" href="/leads">
          <ChevronLeft size={16} /> Back to leads
        </Link>
        <div className="nav">
          {user ? <span className="muted">Signed in as {user.email}</span> : null}
          <button className="text-button" type="button" onClick={logout}>
            <LogOut size={15} /> Log out
          </button>
        </div>
      </div>

      {loading ? <div className="panel">Loading lead...</div> : null}
      {error ? (
        <div className="message error" role="alert">
          {error}
        </div>
      ) : null}

      {lead ? (
        <section className="detail">
          <div className="panel facts">
            <h1 style={{ margin: 0 }}>
              {lead.first_name} {lead.last_name}
            </h1>
            <Fact label="Email" value={lead.email} />
            <div className="fact">
              <strong>Resume / CV</strong>
              <div className="inline-action">
                <span>{lead.resume_filename}</span>
                <button className="text-button" type="button" onClick={onDownloadResume} disabled={downloading}>
                  <Download size={15} />
                  {downloading ? "Downloading" : "Download"}
                </button>
              </div>
            </div>
            <Fact label="Submitted" value={new Date(lead.created_at).toLocaleString()} />
            {lead.assigned_attorney_email ? <Fact label="Assigned attorney" value={lead.assigned_attorney_email} /> : null}
            {lead.assigned_at ? <Fact label="Assigned" value={new Date(lead.assigned_at).toLocaleString()} /> : null}
            <Fact label="Last updated" value={new Date(lead.updated_at).toLocaleString()} />
          </div>

          <aside className="panel facts" aria-label="Lead state">
            <span className={`badge ${lead.state === "PENDING" ? "pending" : "reached"}`}>
              {lead.state.replace("_", " ")}
            </span>
            {lead.reached_out_at ? (
              <p className="muted">
                Reached out by {lead.reached_out_by} on {new Date(lead.reached_out_at).toLocaleString()}.
              </p>
            ) : (
              <p className="muted">This lead is waiting for attorney follow-up.</p>
            )}
            <button className="button secondary" type="button" onClick={onMarkReachedOut} disabled={saving || lead.state === "REACHED_OUT"}>
              <CheckCircle2 size={18} />
              {saving ? "Updating" : "Mark reached out"}
            </button>
          </aside>
        </section>
      ) : null}
    </main>
  );
}

function Fact({ label, value }: { label: string; value: string }) {
  return (
    <div className="fact">
      <strong>{label}</strong>
      <span>{value}</span>
    </div>
  );
}
