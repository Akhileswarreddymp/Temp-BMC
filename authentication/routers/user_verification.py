from fastapi import APIRouter, HTTPException
from authentication.models.api.otp_validation import EmailValidation
from authentication.crud.email_service import EmailService
from authentication.utils.constants import EMAIL_SUBJECT
from authentication.models.api.otp_validation import RedisOtp, SuccessResponse
from authentication.crud.otp_verification import OtpValidator
router = APIRouter(
    prefix="/otp",
    responses={404: {"description": "Not found"}},
    tags=["OTP"],
)


@router.post("/send-email-otp/")
async def send_email(email_data: EmailValidation):
    resp_obj = EmailService()
    response = await resp_obj.send_email(email_data.email_id, EMAIL_SUBJECT)

    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])

    return response

@router.post("/validate-otp")
async def validate_otp(request: RedisOtp):
    resp_obj = OtpValidator()
    try:
        response = await resp_obj.verify_otp(request.key,request.otp)

        if response:
            return SuccessResponse(
                message="Otp Verified Successfully"
            )
        
        return HTTPException(
            status_code=401,
            detail="Invalid Otp"
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Otp validation failed : {error}"
        ) from error