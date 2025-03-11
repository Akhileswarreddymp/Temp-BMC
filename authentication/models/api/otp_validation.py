from pydantic import BaseModel


class EmailValidation(BaseModel):
    email_id: str
