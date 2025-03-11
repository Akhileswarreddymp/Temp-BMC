from pydantic import BaseModel


class EmailValidation(BaseModel):
    email_id: str

class RedisOtp(BaseModel):
    key: str
    otp: int