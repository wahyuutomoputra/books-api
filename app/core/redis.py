import redis
from app.core.config import REDIS_URL

redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)
