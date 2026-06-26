from io import BytesIO
import os
from pathlib import Path
import tempfile

data_dir = Path(tempfile.mkdtemp(prefix="lead-crm-test-"))
os.environ["DATABASE_URL"] = f"sqlite:///{data_dir / 'test.db'}"
os.environ["UPLOAD_DIR"] = str(data_dir / "uploads")
os.environ["OUTBOX_DIR"] = str(data_dir / "outbox")
os.environ["AUTH_SECRET"] = "test-secret"
os.environ["BOOTSTRAP_ADMIN_EMAIL"] = "admin@example.com"
os.environ["BOOTSTRAP_ADMIN_PASSWORD"] = "change-me-admin"

from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.core.security import hash_password
from app.db.session import SessionLocal, init_db
from app.main import app
from app.models.user import User, UserRole
from app.services.users import ensure_bootstrap_admin, get_user_by_email


client = TestClient(app)
init_db()
with SessionLocal() as db:
    ensure_bootstrap_admin(db)


def create_active_attorney(email: str, full_name: str = "Test Attorney") -> None:
    with SessionLocal() as db:
        if get_user_by_email(db, email) is not None:
            return
        db.add(
            User(
                full_name=full_name,
                email=email.lower(),
                password_hash=hash_password("change-me-attorney"),
                role=UserRole.ATTORNEY,
                is_active=True,
            )
        )
        db.commit()


def login(email: str, password: str) -> dict[str, str]:
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_create_lead_requires_resume_type() -> None:
    response = client.post(
        "/api/leads",
        data={"first_name": "Ada", "last_name": "Lovelace", "email": "ada@example.com"},
        files={"resume": ("resume.txt", BytesIO(b"hello"), "text/plain")},
    )

    assert response.status_code == 400


def test_create_list_and_mark_reached_out() -> None:
    create_active_attorney("attorney-one@example.com", "Attorney One")
    create_response = client.post(
        "/api/leads",
        data={"first_name": "Ada", "last_name": "Lovelace", "email": "ada@example.com"},
        files={"resume": ("resume.pdf", BytesIO(b"%PDF-1.4"), "application/pdf")},
    )

    assert create_response.status_code == 201
    lead_id = create_response.json()["id"]
    assert create_response.json()["state"] == "PENDING"
    assert len(list((data_dir / "outbox").glob("*.txt"))) == 2

    headers = login("attorney-one@example.com", "change-me-attorney")

    me_response = client.get("/api/auth/me", headers=headers)
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "attorney-one@example.com"
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


def test_attorney_registration_requires_admin_approval() -> None:
    register_response = client.post(
        "/api/auth/register",
        json={"full_name": "New Attorney", "email": "new-attorney@example.com", "password": "change-me-attorney"},
    )
    assert register_response.status_code == 201
    assert register_response.json()["role"] == "PENDING_ATTORNEY"

    repeat_register_response = client.post(
        "/api/auth/register",
        json={"full_name": "New Attorney", "email": "new-attorney@example.com", "password": "change-me-attorney"},
    )
    assert repeat_register_response.status_code == 201
    assert repeat_register_response.json()["role"] == "PENDING_ATTORNEY"

    pending_login = client.post(
        "/api/auth/login",
        json={"email": "new-attorney@example.com", "password": "change-me-attorney"},
    )
    assert pending_login.status_code == 401

    admin_headers = login("admin@example.com", "change-me-admin")
    attorneys_response = client.get("/api/auth/attorneys", headers=admin_headers)
    assert attorneys_response.status_code == 200
    attorney = next(item for item in attorneys_response.json()["attorneys"] if item["email"] == "new-attorney@example.com")

    approve_response = client.patch(f"/api/auth/attorneys/{attorney['id']}/approve", headers=admin_headers)
    assert approve_response.status_code == 200
    assert approve_response.json()["role"] == "ATTORNEY"

    approved_headers = login("new-attorney@example.com", "change-me-attorney")
    me_response = client.get("/api/auth/me", headers=approved_headers)
    assert me_response.status_code == 200


def test_lead_assignment_uses_least_loaded_active_attorney() -> None:
    create_active_attorney("capacity-a@example.com", "Capacity A")
    create_active_attorney("capacity-b@example.com", "Capacity B")

    first_response = client.post(
        "/api/leads",
        data={"first_name": "First", "last_name": "Lead", "email": "first@example.com"},
        files={"resume": ("resume.pdf", BytesIO(b"%PDF-1.4"), "application/pdf")},
    )
    second_response = client.post(
        "/api/leads",
        data={"first_name": "Second", "last_name": "Lead", "email": "second@example.com"},
        files={"resume": ("resume.pdf", BytesIO(b"%PDF-1.4"), "application/pdf")},
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    admin_headers = login("admin@example.com", "change-me-admin")
    list_response = client.get("/api/leads", headers=admin_headers)
    assert list_response.status_code == 200
    created = [lead for lead in list_response.json()["leads"] if lead["email"] in {"first@example.com", "second@example.com"}]
    assigned_emails = {lead["assigned_attorney_email"] for lead in created}
    assert assigned_emails == {"capacity-a@example.com", "capacity-b@example.com"}

    outbox_text = "\n".join(path.read_text(encoding="utf-8") for path in (data_dir / "outbox").glob("*.txt"))
    assert "First name:" in outbox_text
    assert "Last name:" in outbox_text
    assert "Email:" in outbox_text
    assert "Customer name:" in outbox_text
    assert "Customer email:" in outbox_text
    assert "Lead ID:" in outbox_text
    assert "Resume/CV:" in outbox_text
    assert "Assigned at:" in outbox_text


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
