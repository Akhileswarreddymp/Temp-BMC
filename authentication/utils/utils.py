import random
from authentication.dependencies.redis_connection import get_redis_client

async def generate_otp():
    return str(random.randint(1000, 9999))

