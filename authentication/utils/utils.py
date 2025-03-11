import random

from authentication.dependencies.redis_connection import get_redis_client
from authentication.models.api.otp_validation import RedisOtp

async def generate_otp():
    return str(random.randint(1000, 9999))

async def store_otp_in_redis(request: RedisOtp) -> bool:
    """Store OTP in Redis with a 5-minute expiry."""
    redis_client = await get_redis_client()
    await redis_client.set(request.key, request.otp, ex=300)
    
    return True