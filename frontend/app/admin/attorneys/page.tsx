"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { CheckCircle2, ChevronLeft, LogOut, RefreshCw, ShieldCheck } from "lucide-react";
import {
  ApiError,
  approveAttorney,
  Attorney,
  AuthUser,
  clearToken,
  fetchAttorneys,
  getToken,
  verifySession
} from "@/lib/api";
import { useRouter } from "next/navigation";

export default function AttorneyManagementPage() {
  const router = useRouter();
  const [attorneys, setAttorneys] = useState<Attorney[]>([]);
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [approvingId, setApprovingId] = useState("");
  const [error, setError] = useState("");

  const loadAttorneys = useCallback(async () => {
    if (!getToken()) {
      router.push("/login");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const currentUser = await verifySession();
      setUser(currentUser);
      if (currentUser.role !== "ADMIN") {
        setAttorneys([]);
        setError("Admin access is required to manage attorney approvals.");
        return;
      }
      setAttorneys(await fetchAttorneys());
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to load attorneys.");
      if (caught instanceof ApiError && caught.status === 401) {
        clearToken();
        router.push("/login");
      }
    } finally {
      setLoading(false);
    }
  }, [router]);

  useEffect(() => {
    loadAttorneys();
  }, [loadAttorneys]);

  async function onApprove(attorneyId: string) {
    setApprovingId(attorneyId);
    setError("");
    try {
      await approveAttorney(attorneyId);
      setAttorneys(await fetchAttorneys());
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to approve attorney.");
    } finally {
      setApprovingId("");
    }
  }

  function logout() {
    clearToken();
    router.push("/login");
  }

  return (
    <main className="container">
      <div className="toolbar">
        <div>
          <Link className="text-button" href="/leads">
            <ChevronLeft size={16} /> Back to leads
          </Link>
          <h1 style={{ marginTop: 12 }}>Attorney management</h1>
        </div>
        <div className="nav">
          {user ? <span className="muted">Signed in as {user.email}</span> : null}
          <button className="text-button" type="button" onClick={loadAttorneys}>
            <RefreshCw size={15} /> Refresh
          </button>
          <button className="text-button" type="button" onClick={logout}>
            <LogOut size={15} /> Log out
          </button>
        </div>
      </div>

      {loading ? <div className="panel">Loading attorneys...</div> : null}
      {error ? (
        <div className="message error" role="alert">
          {error}
          {user?.role !== "ADMIN" ? (
            <Link className="text-button" href="/leads">
              Return to leads
            </Link>
          ) : null}
        </div>
      ) : null}
      {!loading && !error && attorneys.length === 0 ? <div className="panel">No attorney accounts have been registered yet.</div> : null}

      <section className="grid" aria-label="Attorney accounts">
        {attorneys.map((attorney) => (
          <article className="card" key={attorney.id}>
            <div>
              <div className="name">{attorney.full_name}</div>
              <div className="muted">{attorney.email}</div>
              <div className="muted">
                Last assigned: {attorney.last_assigned_at ? new Date(attorney.last_assigned_at).toLocaleString() : "Never"}
              </div>
            </div>
            <StatusBadge attorney={attorney} />
            {attorney.role === "PENDING_ATTORNEY" ? (
              <button className="button" type="button" onClick={() => onApprove(attorney.id)} disabled={approvingId === attorney.id}>
                <CheckCircle2 size={18} />
                {approvingId === attorney.id ? "Approving" : "Approve"}
              </button>
            ) : (
              <span className="text-button">
                <ShieldCheck size={15} /> Active
              </span>
            )}
          </article>
        ))}
      </section>
    </main>
  );
}

function StatusBadge({ attorney }: { attorney: Attorney }) {
  if (attorney.role === "PENDING_ATTORNEY") {
    return <span className="badge pending">Pending approval</span>;
  }
  return <span className="badge reached">{attorney.is_active ? "Approved" : "Inactive"}</span>;
}
