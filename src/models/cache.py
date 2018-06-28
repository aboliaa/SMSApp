import redis

from config import REDIS_HOST, REDIS_PORT, REDIS_DB
from utils.log import logger

class Cache(object):
    def set(self, key, val='', expiry=None):
        raise NotImplemented

    def get(self, key):
        raise NotImplemented

    def exists(self, key):
        raise NotImplemented

class RedisClient(object):
    @staticmethod
    def client():
        return redis.StrictRedis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB
        )

def handle_connection_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except redis.exceptions.ConnectionError, e:
            logger.error('Error in connecting to Redis server: {}'.format(str(e)))
            raise ValueError()
    return wrapper

class RedisCache(Cache):
    def __init__(self):
        self.rediscli = RedisClient.client()

    @handle_connection_error
    def set(self, key, val='', expiry=None):
        self.rediscli.set(key, val, expiry)

    @handle_connection_error
    def get(self, key):
        return self.rediscli.get(key)

    @handle_connection_error
    def exists(self, key):
        return self.rediscli.ttl(key) > 0

cache = RedisCache()