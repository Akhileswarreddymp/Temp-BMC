from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from fastapi import HTTPException
from jinja2 import Template
from authentication.settings import Settings
from authentication.utils.utils import generate_otp, store_otp_in_redis
from authentication.models.api.otp_validation import RedisOtp, SuccessResponse

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
    async def send_email(to_email: str, subject: str)-> SuccessResponse:
        settings = Settings()
        try:
            otp = await generate_otp()
            body = await EmailService.render_otp_email(otp)

            msg = MIMEMultipart()
            msg["From"] = settings.SMTP_FROM_EMAIL
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))

            smtp = aiosmtplib.SMTP(
                hostname=settings.SMTP_SERVER, port=settings.SMTP_PORT, use_tls=True
            )
            await smtp.connect()
            await smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            await smtp.sendmail(settings.SMTP_FROM_EMAIL, to_email, msg.as_string())
            await smtp.quit()
            
            data = RedisOtp(
                key=f'{to_email}_otp',
                otp=otp
            )
            await store_otp_in_redis(data)

            return SuccessResponse(
                message= "Email sent Successfully"
            )

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while sending email: {error}",
            ) from error
