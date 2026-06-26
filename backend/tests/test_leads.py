from io import BytesIO
import os
from pathlib import Path
import tempfile

data_dir = Path(tempfile.mkdtemp(prefix="lead-crm-test-"))
os.environ["DATABASE_URL"] = f"sqlite:///{data_dir / 'test.db'}"
os.environ["UPLOAD_DIR"] = str(data_dir / "uploads")
os.environ["OUTBOX_DIR"] = str(data_dir / "outbox")
os.environ["AUTH_SECRET"] = "test-secret"
os.environ["INTERNAL_EMAIL"] = "attorney@example.com"
os.environ["INTERNAL_PASSWORD"] = "change-me"

from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.db.session import SessionLocal, init_db
from app.main import app
from app.services.users import ensure_initial_attorney


client = TestClient(app)
init_db()
with SessionLocal() as db:
    ensure_initial_attorney(db)


def test_create_lead_requires_resume_type() -> None:
    response = client.post(
        "/api/leads",
        data={"first_name": "Ada", "last_name": "Lovelace", "email": "ada@example.com"},
        files={"resume": ("resume.txt", BytesIO(b"hello"), "text/plain")},
    )

    assert response.status_code == 400


def test_create_list_and_mark_reached_out() -> None:
    create_response = client.post(
        "/api/leads",
        data={"first_name": "Ada", "last_name": "Lovelace", "email": "ada@example.com"},
        files={"resume": ("resume.pdf", BytesIO(b"%PDF-1.4"), "application/pdf")},
    )

    assert create_response.status_code == 201
    lead_id = create_response.json()["id"]
    assert create_response.json()["state"] == "PENDING"
    assert len(list((data_dir / "outbox").glob("*.txt"))) == 2

    settings = get_settings()
    login_response = client.post(
        "/api/auth/login",
        json={"email": str(settings.internal_email), "password": settings.internal_password},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    me_response = client.get("/api/auth/me", headers=headers)
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "attorney@example.com"
    assert me_response.json()["role"] == "ATTORNEY"

    list_response = client.get("/api/leads", headers=headers)
    assert list_response.status_code == 200
    assert any(lead["id"] == lead_id for lead in list_response.json()["leads"])

    mark_response = client.patch(f"/api/leads/{lead_id}/reach-out", headers=headers)
    assert mark_response.status_code == 200
    assert mark_response.json()["state"] == "REACHED_OUT"

    resume_response = client.get(f"/api/leads/{lead_id}/resume", headers=headers)
    assert resume_response.status_code == 200
    assert resume_response.content == b"%PDF-1.4"


def test_internal_routes_require_auth() -> None:
    list_response = client.get("/api/leads")
    assert list_response.status_code == 401

    me_response = client.get("/api/auth/me")
    assert me_response.status_code == 401


def test_create_lead_requires_valid_email() -> None:
    response = client.post(
        "/api/leads",
        data={"first_name": "Ada", "last_name": "Lovelace", "email": "not-an-email"},
        files={"resume": ("resume.pdf", BytesIO(b"%PDF-1.4"), "application/pdf")},
    )

    assert response.status_code == 422
