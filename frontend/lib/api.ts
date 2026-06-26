export type LeadState = "PENDING" | "REACHED_OUT";

export type Lead = {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  resume_filename: string;
  resume_content_type: string;
  state: LeadState;
  created_at: string;
  updated_at: string;
  reached_out_at: string | null;
  reached_out_by: string | null;
};

export type AuthUser = {
  email: string;
  role: "ATTORNEY" | "ADMIN";
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";
const TOKEN_KEY = "lead-crm-token";

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  window.localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  window.localStorage.removeItem(TOKEN_KEY);
}

export async function submitLead(formData: FormData): Promise<{ id: string; message: string }> {
  const response = await fetch(`${API_URL}/leads`, {
    method: "POST",
    body: formData
  });
  return parseResponse(response);
}

export async function login(email: string, password: string): Promise<string> {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });
  const payload = await parseResponse<{ access_token: string }>(response);
  return payload.access_token;
}

export async function verifySession(): Promise<AuthUser> {
  const response = await fetch(`${API_URL}/auth/me`, {
    headers: authHeaders()
  });
  return parseResponse<AuthUser>(response);
}

export async function fetchLeads(): Promise<Lead[]> {
  const response = await fetch(`${API_URL}/leads`, {
    headers: authHeaders()
  });
  const payload = await parseResponse<{ leads: Lead[] }>(response);
  return payload.leads;
}

export async function fetchLead(id: string): Promise<Lead> {
  const response = await fetch(`${API_URL}/leads/${id}`, {
    headers: authHeaders()
  });
  return parseResponse<Lead>(response);
}

export async function markReachedOut(id: string): Promise<Lead> {
  const response = await fetch(`${API_URL}/leads/${id}/reach-out`, {
    method: "PATCH",
    headers: authHeaders()
  });
  return parseResponse<Lead>(response);
}

export async function downloadResume(id: string): Promise<Blob> {
  const response = await fetch(`${API_URL}/leads/${id}/resume`, {
    headers: authHeaders()
  });
  if (response.ok) return response.blob();
  throw await parseResponse<never>(response);
}

function authHeaders(): HeadersInit {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function parseResponse<T>(response: Response): Promise<T> {
  if (response.ok) return response.json() as Promise<T>;
  let detail = "Request failed";
  try {
    const payload = await response.json();
    if (typeof payload.detail === "string") {
      detail = payload.detail;
    } else if (Array.isArray(payload.detail)) {
      detail = payload.detail
        .map((item: { msg?: string; loc?: string[] }) => {
          const field = Array.isArray(item.loc) ? item.loc[item.loc.length - 1] : undefined;
          return field && item.msg ? `${field}: ${item.msg}` : item.msg;
        })
        .filter(Boolean)
        .join("; ");
    }
  } catch {
    detail = response.statusText || detail;
  }
  throw new ApiError(detail || "Request failed", response.status);
}
