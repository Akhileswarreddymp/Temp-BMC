from fastapi import HTTPException
from authentication.dependencies.redis_connection import get_redis_client
from authentication.models.api.otp_validation import RedisOtp


class OtpValidator:
    async def verify_otp(self,key: str, otp: str):
        try:
            redis_client= await get_redis_client()
            otp_in_redis = await redis_client.get(f"{key}_otp")

            if otp_in_redis == otp:
                return True
            return False
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Exception occured while validating otp {error}"
            )
