from fast_agend.core.config import settings
import smtplib
from email.message import EmailMessage

class EmailService:
    def send_reset_password_email(self, email: str, reset_link: str):
        message = EmailMessage()
        message["Subject"] = "Redefinição de senha"
        message["From"] = settings.MAIL_FROM
        message["To"] = email
        message.set_content(
            f"Clique no link para redefinir sua senha:\n{reset_link}"
        )

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(message)