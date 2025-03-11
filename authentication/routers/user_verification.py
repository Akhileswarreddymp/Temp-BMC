from fastapi import APIRouter, HTTPException
from authentication.models.api.otp_validation import EmailValidation
from authentication.crud.user_verify import EmailService
from authentication.utils.constants import EMAIL_SUBJECT


router = APIRouter(
    prefix="/otp",
    responses={404: {"description": "Not found"}},
    tags=["OTP"],
)


@router.post("/send-email-otp/")
async def send_email(email_data: EmailValidation):
    response = await EmailService.send_email(email_data.email_id, EMAIL_SUBJECT)

    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])

    return response
