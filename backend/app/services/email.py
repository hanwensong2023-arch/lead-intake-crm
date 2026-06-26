from dataclasses import dataclass
from datetime import UTC, datetime
from email.message import EmailMessage
import json
import logging
import smtplib
import time
from urllib import error, request
from uuid import uuid4

from app.core.config import get_settings
from app.models.lead import Lead
from app.models.user import User


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Email:
    to: str
    subject: str
    body: str


class EmailService:
    def send(self, message: Email) -> None:
        settings = get_settings()
        if settings.mailtrap_api_token:
            try:
                self._send_mailtrap_api(message)
                logger.info("Email sent via Mailtrap API to=%s subject=%s", message.to, message.subject)
            except (OSError, RuntimeError) as exc:
                self._write_to_outbox(message)
                logger.warning(
                    "Mailtrap API send failed; wrote email to outbox to=%s subject=%s error=%s",
                    message.to,
                    message.subject,
                    exc,
                )
            return
        if settings.smtp_host:
            try:
                self._send_smtp(message)
                logger.info("Email sent via SMTP to=%s subject=%s", message.to, message.subject)
            except (OSError, smtplib.SMTPException):
                self._write_to_outbox(message)
                logger.exception("SMTP send failed; wrote email to outbox to=%s subject=%s", message.to, message.subject)
            return
        self._write_to_outbox(message)
        logger.info("Email written to local outbox to=%s subject=%s", message.to, message.subject)

    def send_lead_notifications(self, lead: Lead, assigned_attorney: User) -> None:
        prospect = Email(
            to=lead.email,
            subject="We received your information",
            body=(
                f"Hi {lead.first_name},\n\n"
                "Thanks for reaching out to Alma. We received your information successfully "
                "and our team will review your submission shortly.\n\n"
                "Submission received:\n"
                f"First name: {lead.first_name}\n"
                f"Last name: {lead.last_name}\n"
                f"Email: {lead.email}\n"
                f"Resume/CV: {lead.resume_filename}\n\n"
                "Best,\nAlma"
            ),
        )
        attorney_notification = Email(
            to=assigned_attorney.email,
            subject=f"New lead submitted: {lead.first_name} {lead.last_name}",
            body=(
                "A new Alma lead has been assigned to you.\n\n"
                f"Customer name: {lead.first_name} {lead.last_name}\n"
                f"Customer email: {lead.email}\n"
                f"Lead ID: {lead.id}\n"
                f"Resume/CV: {lead.resume_filename}\n"
                f"Assigned at: {lead.assigned_at.isoformat() if lead.assigned_at else 'not recorded'}\n"
            ),
        )
        settings = get_settings()
        self.send(prospect)
        if settings.mailtrap_api_token and settings.mailtrap_use_sandbox and settings.mailtrap_send_delay_seconds > 0:
            time.sleep(settings.mailtrap_send_delay_seconds)
        self.send(attorney_notification)

    def _send_mailtrap_api(self, message: Email) -> None:
        settings = get_settings()
        api_url = settings.mailtrap_api_url
        if settings.mailtrap_use_sandbox:
            if settings.mailtrap_inbox_id is None:
                raise RuntimeError("MAILTRAP_INBOX_ID is required when MAILTRAP_USE_SANDBOX=true.")
            api_url = f"https://sandbox.api.mailtrap.io/api/send/{settings.mailtrap_inbox_id}"
        payload = {
            "from": {"email": str(settings.mailtrap_from_email), "name": settings.mailtrap_from_name},
            "to": [{"email": message.to}],
            "subject": message.subject,
            "text": message.body,
            "category": "Lead Intake CRM",
        }
        api_request = request.Request(
            api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {settings.mailtrap_api_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "lead-intake-crm/1.0",
            },
            method="POST",
        )
        for attempt in range(3):
            try:
                with request.urlopen(api_request, timeout=15) as response:
                    if response.status >= 400:
                        raise RuntimeError(f"Mailtrap API returned HTTP {response.status}")
                return
            except error.HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")
                if exc.code == 429 and attempt < 2:
                    time.sleep(1.2 * (attempt + 1))
                    continue
                raise RuntimeError(f"Mailtrap API returned HTTP {exc.code}: {detail}") from exc

    def _send_smtp(self, message: Email) -> None:
        settings = get_settings()
        email = EmailMessage()
        email["From"] = str(settings.smtp_from_email)
        email["To"] = message.to
        email["Subject"] = message.subject
        email.set_content(message.body)

        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
            if settings.smtp_use_tls:
                smtp.starttls()
            if settings.smtp_username and settings.smtp_password:
                smtp.login(settings.smtp_username, settings.smtp_password)
            smtp.send_message(email)

    def _write_to_outbox(self, message: Email) -> None:
        settings = get_settings()
        filename = f"{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}-{uuid4()}.txt"
        path = settings.outbox_dir / filename
        path.write_text(
            f"To: {message.to}\nSubject: {message.subject}\n\n{message.body}\n",
            encoding="utf-8",
        )
