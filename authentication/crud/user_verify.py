import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from authentication.settings import Settings
from jinja2 import Template

from authentication.utils.utils import generate_otp

class EmailService:
    @staticmethod
    async def render_otp_email(otp: str) -> str:
        """Loads and renders the OTP email template from a file."""
        try:
            with open("templates/otp_email.html", "r") as file:
                template = Template(file.read())
            return template.render(otp=otp)
        except FileNotFoundError:
            return f"<p>Hello Welcome to BMC, your OTP is: <b>{otp}</b></p>"



    @staticmethod
    async def send_email(to_email: str, subject: str):
        settings = Settings()
        try:
            otp = await generate_otp()
            msg = MIMEMultipart()
            body = await EmailService.render_otp_email(otp)
            msg["From"] = settings.SMTP_FROM_EMAIL
            msg["To"] = to_email
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "html"))  # Send as HTML

            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                server.sendmail(settings.SMTP_FROM_EMAIL, to_email, msg.as_string())

            return {"message": "Email sent successfully"}

        except Exception as e:
            return {"error": str(e)}
