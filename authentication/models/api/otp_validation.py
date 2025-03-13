from pydantic import BaseModel


class EmailValidation(BaseModel):
    email_id: str

class RedisOtp(BaseModel):
    key: str
    otp: str

class SuccessResponse(BaseModel):
    message: str