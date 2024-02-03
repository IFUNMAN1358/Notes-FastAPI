from redis.asyncio import StrictRedis

from app.config import Config


async def get_redis():
    redis = await StrictRedis(host=Config.redis_host,
                              port=Config.redis_port,
                              decode_responses=True,
                              protocol=3,
                              db=0)
    try:
        yield redis
    finally:
        await redis.aclose()
