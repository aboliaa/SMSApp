import redis

from config import REDIS_HOST, REDIS_PORT, REDIS_DB
from utils.log import logger

class RedisClient(redis.StrictRedis):
    def __init__(self):
        super(RedisClient, self).__init__(
            host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB
        )

def handle_connection_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except redis.exceptions.ConnectionError, e:
            logger.error('Error in connecting to Redis server: {}'.format(str(e)))
            raise ValueError()
    return wrapper
