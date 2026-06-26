from dataclasses import dataclass
from datetime import UTC, datetime
from email.message import EmailMessage
import smtplib
from uuid import uuid4

from app.core.config import get_settings
from app.models.lead import Lead


@dataclass(frozen=True)
class Email:
    to: str
    subject: str
    body: str


class EmailService:
    def send(self, message: Email) -> None:
        settings = get_settings()
        if settings.smtp_host:
            self._send_smtp(message)
            return
        self._write_to_outbox(message)

    def send_lead_notifications(self, lead: Lead) -> None:
        settings = get_settings()
        prospect = Email(
            to=lead.email,
            subject="We received your information",
            body=(
                f"Hi {lead.first_name},\n\n"
                "Thanks for reaching out. Our team has received your information and will review it shortly.\n\n"
                "Best,\nLead Intake Team"
            ),
        )
        attorney = Email(
            to=str(settings.internal_email),
            subject=f"New lead submitted: {lead.first_name} {lead.last_name}",
            body=(
                "A new lead was submitted.\n\n"
                f"Name: {lead.first_name} {lead.last_name}\n"
                f"Email: {lead.email}\n"
                f"Resume: {lead.resume_filename}\n"
                f"Lead ID: {lead.id}\n"
            ),
        )
        self.send(prospect)
        self.send(attorney)

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
