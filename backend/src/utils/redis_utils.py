import logging
import redis
from src.utils import Config

logger = logging.getLogger(__name__)

config = Config()

redis_client = redis.Redis(host=config.redis_host, port=6379)

def test_redis_connection():
    connection_healthy = False
    try:
        ping_response = redis_client.ping()
        connection_healthy = ping_response

    except Exception as e:
        logger.exception(f"Redis connection failed: {e}")

    finally:
        redis_client.close()
        return connection_healthy
